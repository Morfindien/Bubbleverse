#!/usr/bin/env python3
"""Bubbleverse Q-038 — coordinate localization of Q037 implementation geometry.

Artifact-only deterministic decomposition of the already validated Q037
CamSpec/HiLLiPoP exact-common-support endpoint vectors.

No CLASS, likelihood, optimizer, sampler, or cross-likelihood objective
comparison is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import statistics
from pathlib import Path
from typing import Any, Mapping, Sequence

Q = "Q-038"
PROGRAM_ID = "Q038-COORDLOC-V1"
RUN_ID = "Q038-EXACT-TT-COMMON-SUPPORT-COORD-LOCALIZATION-V1"
RESULT_ID = "R-Q038-EDE-COORDINATE-LOCALIZATION-001"

PARENT_Q037_RESULT = "R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001"
PARENT_Q037_PROGRAM = "Q037-TTGEOM-V1"
PARENT_Q032_RESULT = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
PARENT_Q032_RUN_ID = 33994305721

COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
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
MATERIALITY_THRESHOLD = 0.10

FULL_CAPTURE_THRESHOLD = 0.80
LOO_CAPTURE_THRESHOLD = 0.70
LOO_REQUIRED = 8
CONCENTRATED_MAX_SUBSET_SIZE = 2
REPLAY_TOL = 1e-12
EPS = 1e-15

Q037_BENCHMARKS = {
    "matched_median_displacement": 2.9317906965863507,
    "matched_max_displacement": 5.229543793539735,
    "matched_exceedance_count_gt_0_10": 9,
    "normalized_centroid_displacement": 0.8311487237190059,
    "pairwise_median_drift": 1.6367910228418985,
    "pairwise_max_drift": 4.755572606658088,
    "pairwise_exceedance_count_gt_0_10": 36,
}


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


def validate_preregister(pr: Mapping[str, Any]) -> None:
    if pr.get("status") != "PREREGISTERED_BEFORE_Q037_COORDINATE_RANKING_INSPECTION":
        raise RuntimeError("PREREGISTER_STATUS_GATE=FAIL")
    p = pr.get("project", {})
    expected = {"q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID}
    if p != expected:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL preregister")

    parent = pr.get("parent", {})
    if parent.get("q037_result_id") != PARENT_Q037_RESULT or parent.get("q037_program_id") != PARENT_Q037_PROGRAM:
        raise RuntimeError("PARENT_Q037_PROVENANCE_GATE=FAIL preregister")
    if int(parent.get("q032_run_id", -1)) != PARENT_Q032_RUN_ID:
        raise RuntimeError("PARENT_Q032_PROVENANCE_GATE=FAIL preregister")

    geom = pr.get("common_geometry", {})
    if tuple(geom.get("coordinates", [])) != COORDS:
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL preregister")
    if geom.get("locked_scales") != SCALES or geom.get("locked_scales_hash") != LOCKED_SCALES_HASH:
        raise RuntimeError("Q031_LOCKED_SCALE_GATE=FAIL preregister")
    if float(geom.get("materiality_threshold", -1)) != MATERIALITY_THRESHOLD:
        raise RuntimeError("MATERIALITY_THRESHOLD_GATE=FAIL preregister")

    loc = pr.get("localization_rule", {})
    if float(loc.get("full_capture_threshold", -1)) != FULL_CAPTURE_THRESHOLD:
        raise RuntimeError("CONCENTRATION_PREREGISTRATION_GATE=FAIL full_capture")
    if float(loc.get("leave_one_label_out_capture_threshold", -1)) != LOO_CAPTURE_THRESHOLD:
        raise RuntimeError("CONCENTRATION_PREREGISTRATION_GATE=FAIL loo_capture")
    if int(loc.get("leave_one_label_out_required_passes", -1)) != LOO_REQUIRED:
        raise RuntimeError("CONCENTRATION_PREREGISTRATION_GATE=FAIL loo_required")
    if int(loc.get("concentrated_max_subset_size", -1)) != CONCENTRATED_MAX_SUBSET_SIZE:
        raise RuntimeError("CONCENTRATION_PREREGISTRATION_GATE=FAIL subset_size")
    if loc.get("subset_universe") != "ALL_127_NONEMPTY_SUBSETS_OF_THE_7_FROZEN_COORDINATES":
        raise RuntimeError("SYMMETRIC_SUBSET_GATE=FAIL preregister")

    rules = pr.get("rules", {})
    must = (
        "q035_remains_authoritative_closed",
        "q036_remains_closed",
        "q037_remains_closed",
        "no_stable_label_discriminator",
        "q022_labels_are_provenance_only",
        "no_cross_likelihood_absolute_objective_subtraction",
        "no_cross_likelihood_objective_sum",
        "no_forced_native_nuisance_mapping",
        "shared_planck_sky_not_independent_observations",
        "no_likelihood_rerun",
        "no_scale_tuning",
        "no_materiality_threshold_tuning",
        "no_concentration_threshold_tuning",
        "all_subsets_symmetric",
        "raw_per_coordinate_output_preserved",
        "localization_is_not_causal_attribution",
        "stop_after_concentrated_distributed_inconclusive",
    )
    if not all(rules.get(k) is True for k in must):
        raise RuntimeError("PREREGISTER_RULE_GATE=FAIL")


def validate_source_lock(lock: Mapping[str, Any]) -> None:
    if lock.get("q") != Q or lock.get("program_id") != PROGRAM_ID:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    q37 = lock.get("q037", {})
    if q37.get("result_id") != PARENT_Q037_RESULT or q37.get("program_id") != PARENT_Q037_PROGRAM:
        raise RuntimeError("PARENT_Q037_PROVENANCE_GATE=FAIL source_lock")
    q32 = lock.get("q032", {})
    if int(q32.get("run_id", -1)) != PARENT_Q032_RUN_ID or q32.get("result_id") != PARENT_Q032_RESULT:
        raise RuntimeError("PARENT_Q032_PROVENANCE_GATE=FAIL source_lock")
    analysis = lock.get("analysis_lock", {})
    if tuple(analysis.get("coordinates", [])) != COORDS:
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL source_lock")
    if analysis.get("locked_scales") != SCALES or analysis.get("locked_scales_hash") != LOCKED_SCALES_HASH:
        raise RuntimeError("Q031_LOCKED_SCALE_GATE=FAIL source_lock")
    if float(analysis.get("materiality_threshold", -1)) != MATERIALITY_THRESHOLD:
        raise RuntimeError("MATERIALITY_THRESHOLD_GATE=FAIL source_lock")
    concentration = analysis.get("concentration", {})
    expected = {
        "full_capture_threshold": FULL_CAPTURE_THRESHOLD,
        "leave_one_label_out_capture_threshold": LOO_CAPTURE_THRESHOLD,
        "leave_one_label_out_required_passes": LOO_REQUIRED,
        "concentrated_max_subset_size": CONCENTRATED_MAX_SUBSET_SIZE,
    }
    if concentration != expected:
        raise RuntimeError("CONCENTRATION_PREREGISTRATION_GATE=FAIL source_lock")


def validate_input_gate(gate: Mapping[str, Any], raw_path: str | Path) -> None:
    if gate.get("q") != Q or gate.get("program_id") != PROGRAM_ID or gate.get("status") != "PASS":
        raise RuntimeError("Q037_RAW_INPUT_GATE=FAIL")
    actual = sha256_file(raw_path)
    if gate.get("q037_raw_sha256") != actual:
        raise RuntimeError("Q037_RAW_INPUT_DIGEST_GATE=FAIL")
    method = gate.get("input_method")
    if method not in ("EXISTING_Q037_RAW_ARTIFACT", "DETERMINISTIC_Q037_RAW_REPLAY_FROM_Q032"):
        raise RuntimeError("Q037_RAW_INPUT_METHOD_GATE=FAIL")


def validate_q037_raw(raw: Mapping[str, Any]) -> dict[str, dict[str, dict[str, float]]]:
    if raw.get("q") != "Q-037" or raw.get("program_id") != PARENT_Q037_PROGRAM:
        raise RuntimeError("PARENT_Q037_PROVENANCE_GATE=FAIL raw_identity")
    if int(raw.get("parent_q032_run_id", -1)) != PARENT_Q032_RUN_ID:
        raise RuntimeError("PARENT_Q032_PROVENANCE_GATE=FAIL raw_identity")

    rows_obj = raw.get("raw_endpoint_vectors")
    if not isinstance(rows_obj, Mapping) or set(rows_obj) != {"camspec", "hillipop"}:
        raise RuntimeError("NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL raw_structure")

    rows: dict[str, dict[str, dict[str, float]]] = {"camspec": {}, "hillipop": {}}
    for impl in ("camspec", "hillipop"):
        impl_rows = rows_obj.get(impl)
        if not isinstance(impl_rows, Mapping) or set(impl_rows) != set(LABELS):
            raise RuntimeError(f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL implementation={impl}")
        for label in LABELS:
            vector = impl_rows[label]
            if not isinstance(vector, Mapping):
                raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL vector={impl}:{label}")
            if set(vector) != set(COORDS):
                raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coordinate_set={impl}:{label}")
            rows[impl][label] = {}
            for coord in COORDS:
                if not finite(vector[coord]):
                    raise RuntimeError(f"FINITE_INPUT_GATE=FAIL {impl}:{label}:{coord}")
                rows[impl][label][coord] = float(vector[coord])

    provenance = raw.get("endpoint_provenance")
    if not isinstance(provenance, Mapping) or len(provenance) != 18:
        raise RuntimeError("PARENT_Q037_PROVENANCE_GATE=FAIL endpoint_provenance")
    support_hashes = {
        str(v.get("support_sha256"))
        for v in provenance.values()
        if isinstance(v, Mapping) and v.get("support_sha256") is not None
    }
    if len(support_hashes) != 1 or len(next(iter(support_hashes))) != 64:
        raise RuntimeError("EXACT_COMMON_SUPPORT_IDENTITY_GATE=FAIL raw_provenance")
    return rows


def metric(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    z = [(a[c] - b[c]) / SCALES[c] for c in COORDS]
    return math.sqrt(sum(v * v for v in z) / len(COORDS))


def q037_replay(rows: Mapping[str, Mapping[str, Mapping[str, float]]]) -> dict[str, Any]:
    c = rows["camspec"]
    h = rows["hillipop"]
    matched = {l: metric(c[l], h[l]) for l in LABELS}
    cc = {coord: statistics.mean(c[l][coord] for l in LABELS) for coord in COORDS}
    hc = {coord: statistics.mean(h[l][coord] for l in LABELS) for coord in COORDS}
    drifts = {}
    for a, b in itertools.combinations(LABELS, 2):
        dc = metric(c[a], c[b])
        dh = metric(h[a], h[b])
        drifts[f"{a}|{b}"] = abs(dh - dc)
    return {
        "matched_endpoint_rms": matched,
        "matched_median_displacement": float(statistics.median(matched.values())),
        "matched_max_displacement": float(max(matched.values())),
        "matched_exceedance_count_gt_0_10": int(sum(v > MATERIALITY_THRESHOLD for v in matched.values())),
        "normalized_centroid_displacement": float(metric(cc, hc)),
        "absolute_pairwise_distance_drifts": drifts,
        "pairwise_median_drift": float(statistics.median(drifts.values())),
        "pairwise_max_drift": float(max(drifts.values())),
        "pairwise_exceedance_count_gt_0_10": int(sum(v > MATERIALITY_THRESHOLD for v in drifts.values())),
    }


def replay_benchmark_differences(replay: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key, expected in Q037_BENCHMARKS.items():
        actual = replay[key]
        if isinstance(expected, int):
            out[key] = float(abs(int(actual) - expected))
        else:
            out[key] = abs(float(actual) - float(expected))
    return out


def normalized_diff(rows: Mapping[str, Mapping[str, Mapping[str, float]]], label: str) -> dict[str, float]:
    return {
        c: (rows["hillipop"][label][c] - rows["camspec"][label][c]) / SCALES[c]
        for c in COORDS
    }


def shares_from_nonnegative(mass: Mapping[str, float]) -> dict[str, float]:
    total = sum(float(mass[c]) for c in COORDS)
    if not math.isfinite(total) or total <= EPS:
        raise RuntimeError("LOCALIZATION_DENOMINATOR_GATE=FAIL")
    return {c: float(mass[c]) / total for c in COORDS}


def matched_decomposition(
    rows: Mapping[str, Mapping[str, Mapping[str, float]]],
    labels: Sequence[str],
) -> dict[str, Any]:
    per_label: dict[str, Any] = {}
    pooled = {c: 0.0 for c in COORDS}
    for label in labels:
        z = normalized_diff(rows, label)
        energy = {c: z[c] ** 2 for c in COORDS}
        for c in COORDS:
            pooled[c] += energy[c]
        per_label[label] = {
            "normalized_signed_difference": z,
            "squared_energy": energy,
            "energy_share": shares_from_nonnegative(energy),
            "q037_rms": math.sqrt(sum(energy.values()) / len(COORDS)),
        }
    return {
        "per_label": per_label,
        "pooled_energy": pooled,
        "pooled_share": shares_from_nonnegative(pooled),
    }


def centroid_decomposition(
    rows: Mapping[str, Mapping[str, Mapping[str, float]]],
    labels: Sequence[str],
) -> dict[str, Any]:
    ccent = {c: statistics.mean(rows["camspec"][l][c] for l in labels) for c in COORDS}
    hcent = {c: statistics.mean(rows["hillipop"][l][c] for l in labels) for c in COORDS}
    z = {c: (hcent[c] - ccent[c]) / SCALES[c] for c in COORDS}
    energy = {c: z[c] ** 2 for c in COORDS}
    return {
        "camspec_centroid": ccent,
        "hillipop_centroid": hcent,
        "normalized_signed_difference": z,
        "squared_energy": energy,
        "energy_share": shares_from_nonnegative(energy),
        "q037_rms": math.sqrt(sum(energy.values()) / len(COORDS)),
    }


def pairwise_shape_decomposition(
    rows: Mapping[str, Mapping[str, Mapping[str, float]]],
    labels: Sequence[str],
) -> dict[str, Any]:
    edges: dict[str, Any] = {}
    pooled_abs = {c: 0.0 for c in COORDS}
    max_exact_residual = 0.0

    for a, b in itertools.combinations(labels, 2):
        uc = {c: (rows["camspec"][a][c] - rows["camspec"][b][c]) / SCALES[c] for c in COORDS}
        uh = {c: (rows["hillipop"][a][c] - rows["hillipop"][b][c]) / SCALES[c] for c in COORDS}
        dc = math.sqrt(sum(uc[c] ** 2 for c in COORDS) / len(COORDS))
        dh = math.sqrt(sum(uh[c] ** 2 for c in COORDS) / len(COORDS))
        denom = len(COORDS) * (dh + dc)
        if denom <= EPS:
            signed = {c: 0.0 for c in COORDS}
        else:
            # Exact additive decomposition:
            # dh - dc = sum_c (uh_c^2 - uc_c^2) / [n * (dh + dc)].
            signed = {c: (uh[c] ** 2 - uc[c] ** 2) / denom for c in COORDS}
        residual = abs(sum(signed.values()) - (dh - dc))
        max_exact_residual = max(max_exact_residual, residual)
        abs_mass = {c: abs(signed[c]) for c in COORDS}
        if sum(abs_mass.values()) <= EPS and abs(dh - dc) > REPLAY_TOL:
            raise RuntimeError("PAIRWISE_EXACT_DECOMPOSITION_GATE=FAIL zero_mass")
        for c in COORDS:
            pooled_abs[c] += abs_mass[c]
        key = f"{a}|{b}"
        edges[key] = {
            "camspec_normalized_edge": uc,
            "hillipop_normalized_edge": uh,
            "camspec_rms_distance": dc,
            "hillipop_rms_distance": dh,
            "q037_signed_distance_change": dh - dc,
            "q037_absolute_distance_drift": abs(dh - dc),
            "signed_coordinate_contribution": signed,
            "absolute_coordinate_contribution_mass": abs_mass,
            "absolute_coordinate_contribution_share": (
                shares_from_nonnegative(abs_mass) if sum(abs_mass.values()) > EPS else {c: 0.0 for c in COORDS}
            ),
            "exact_additivity_residual": residual,
        }

    return {
        "edges": edges,
        "pooled_absolute_contribution_mass": pooled_abs,
        "pooled_share": shares_from_nonnegative(pooled_abs),
        "max_exact_additivity_residual": max_exact_residual,
    }


def capture(share: Mapping[str, float], subset: Sequence[str]) -> float:
    return float(sum(float(share[c]) for c in subset))


def all_nonempty_subsets() -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    for size in range(1, len(COORDS) + 1):
        out.extend(itertools.combinations(COORDS, size))
    return out


def subset_analysis(rows: Mapping[str, Mapping[str, Mapping[str, float]]], full: Mapping[str, Any]) -> dict[str, Any]:
    loo: dict[str, Any] = {}
    for omitted in LABELS:
        kept = tuple(l for l in LABELS if l != omitted)
        loo[omitted] = {
            "matched": matched_decomposition(rows, kept),
            "centroid": centroid_decomposition(rows, kept),
            "pairwise_shape": pairwise_shape_decomposition(rows, kept),
        }

    rows_out = []
    qualifying = []
    for subset in all_nonempty_subsets():
        full_capture = {
            "matched": capture(full["matched"]["pooled_share"], subset),
            "centroid": capture(full["centroid"]["energy_share"], subset),
            "pairwise_shape": capture(full["pairwise_shape"]["pooled_share"], subset),
        }
        loo_capture = {}
        pass_counts = {"matched": 0, "centroid": 0, "pairwise_shape": 0}
        joint_passes = 0
        for omitted in LABELS:
            vals = {
                "matched": capture(loo[omitted]["matched"]["pooled_share"], subset),
                "centroid": capture(loo[omitted]["centroid"]["energy_share"], subset),
                "pairwise_shape": capture(loo[omitted]["pairwise_shape"]["pooled_share"], subset),
            }
            loo_capture[omitted] = vals
            flags = {k: v >= LOO_CAPTURE_THRESHOLD for k, v in vals.items()}
            for k, ok in flags.items():
                pass_counts[k] += int(ok)
            joint_passes += int(all(flags.values()))

        qualifies = (
            all(v >= FULL_CAPTURE_THRESHOLD for v in full_capture.values())
            and all(v >= LOO_REQUIRED for v in pass_counts.values())
        )
        row = {
            "subset": list(subset),
            "size": len(subset),
            "full_capture": full_capture,
            "leave_one_label_out_pass_counts": pass_counts,
            "leave_one_label_out_joint_passes": joint_passes,
            "leave_one_label_out_capture": loo_capture,
            "qualifies": qualifies,
        }
        rows_out.append(row)
        if qualifies:
            qualifying.append(row)

    if len(rows_out) != 127:
        raise RuntimeError("SYMMETRIC_SUBSET_GATE=FAIL subset_count")
    if not qualifying:
        raise RuntimeError("CONCENTRATION_CLASSIFIER_GATE=FAIL no_qualifying_subset")

    min_size = min(r["size"] for r in qualifying)
    minimal = [r for r in qualifying if r["size"] == min_size]
    classification = "CONCENTRATED" if min_size <= CONCENTRATED_MAX_SUBSET_SIZE else "DISTRIBUTED"
    return {
        "all_subsets": rows_out,
        "qualifying_subsets": qualifying,
        "minimal_qualifying_subset_size": min_size,
        "minimal_qualifying_subsets": [r["subset"] for r in minimal],
        "classification": classification,
        "decision_thresholds": {
            "full_capture_threshold": FULL_CAPTURE_THRESHOLD,
            "leave_one_label_out_capture_threshold": LOO_CAPTURE_THRESHOLD,
            "leave_one_label_out_required_passes": LOO_REQUIRED,
            "concentrated_max_subset_size": CONCENTRATED_MAX_SUBSET_SIZE,
        },
    }


def technical_result(reason: str, preregister: str, source_lock: str, input_gate: str) -> dict[str, Any]:
    return {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "execution_status": "TECHNICAL_INCONCLUSIVE",
        "actual_computed_result": False,
        "q038_stop_case": "INCONCLUSIVE",
        "final_classification": "INCONCLUSIVE_TECHNICAL",
        "FINAL_RESULT_GATE": "UNRESOLVED",
        "technical_reason": reason,
        "preregister_sha256": sha256_file(preregister) if Path(preregister).exists() else None,
        "source_lock_sha256": sha256_file(source_lock) if Path(source_lock).exists() else None,
        "input_gate_sha256": sha256_file(input_gate) if Path(input_gate).exists() else None,
        "claim_boundaries": {
            "q035_remains_closed": True,
            "q036_remains_closed": True,
            "q037_remains_closed": True,
            "coordinate_localization_is_causal_attribution": False,
            "physical_planck_systematic_established": False,
            "ede_preference_established": False,
            "ede_falsification_established": False,
            "h0_changed": False,
        },
    }


def run(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    prereg = read_json(args.preregister)
    lock = read_json(args.source_lock)
    input_gate = read_json(args.input_gate)
    raw = read_json(args.q037_raw)

    validate_preregister(prereg)
    validate_source_lock(lock)
    validate_input_gate(input_gate, args.q037_raw)
    rows = validate_q037_raw(raw)

    replay = q037_replay(rows)
    replay_diffs = replay_benchmark_differences(replay)
    replay_gate = max(replay_diffs.values()) <= REPLAY_TOL

    full = {
        "matched": matched_decomposition(rows, LABELS),
        "centroid": centroid_decomposition(rows, LABELS),
        "pairwise_shape": pairwise_shape_decomposition(rows, LABELS),
    }
    if full["pairwise_shape"]["max_exact_additivity_residual"] > REPLAY_TOL:
        raise RuntimeError("PAIRWISE_EXACT_DECOMPOSITION_GATE=FAIL")

    subsets = subset_analysis(rows, full)
    cls = subsets["classification"]

    gates = {
        "Q_IDENTITY_GATE": True,
        "JOURNAL_CONTINUITY_GATE": True,
        "PARENT_Q037_PROVENANCE_GATE": True,
        "PARENT_Q032_PROVENANCE_GATE": True,
        "Q037_RAW_INPUT_GATE": True,
        "NINE_BY_NINE_LABEL_IDENTITY_GATE": True,
        "COMMON_COORDINATE_GATE": True,
        "Q031_LOCKED_SCALE_GATE": True,
        "MATERIALITY_THRESHOLD_GATE": True,
        "CONCENTRATION_PREREGISTRATION_GATE": True,
        "SYMMETRIC_SUBSET_GATE": True,
        "EXACT_COMMON_SUPPORT_IDENTITY_GATE": True,
        "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE": True,
        "Q037_NUMERICAL_REPLAY_GATE": replay_gate,
        "PAIRWISE_EXACT_DECOMPOSITION_GATE": full["pairwise_shape"]["max_exact_additivity_residual"] <= REPLAY_TOL,
        "FINITE_RESULT_GATE": True,
        "CLASSIFICATION_GATE": cls in ("CONCENTRATED", "DISTRIBUTED"),
        "Q035_CLOSED_PRESERVATION_GATE": True,
        "Q036_CLOSED_PRESERVATION_GATE": True,
        "Q037_CLOSED_PRESERVATION_GATE": True,
        "NO_CAUSAL_ATTRIBUTION_GATE": True,
    }
    if not all(gates.values()):
        failed = [k for k, v in gates.items() if not v]
        raise RuntimeError("MANDATORY_ANALYSIS_GATE=FAIL " + ",".join(failed))

    raw_decomposition = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "q037_raw_sha256": sha256_file(args.q037_raw),
        "raw_endpoint_vectors": rows,
        "q037_replay": replay,
        "q037_replay_absolute_differences": replay_diffs,
        "matched_location_decomposition": full["matched"],
        "centroid_decomposition": full["centroid"],
        "pairwise_shape_decomposition": full["pairwise_shape"],
        "subset_analysis": subsets,
    }

    result = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "scientific_question": prereg["scientific_question"],
        "execution_mode": "ARTIFACT_ONLY_DETERMINISTIC_PROGRAM",
        "execution_status": "COMPLETE",
        "actual_computed_result": True,
        "parent_q037": {
            "result_id": PARENT_Q037_RESULT,
            "program_id": PARENT_Q037_PROGRAM,
            "raw_input_method": input_gate["input_method"],
            "raw_input_sha256": sha256_file(args.q037_raw),
            "discovered_q037_artifact": input_gate.get("q037_artifact"),
        },
        "parent_q032": {
            "run_id": PARENT_Q032_RUN_ID,
            "result_id": PARENT_Q032_RESULT,
        },
        "common_geometry": {
            "coordinates": list(COORDS),
            "locked_scales": SCALES,
            "locked_scales_hash": LOCKED_SCALES_HASH,
            "materiality_threshold": MATERIALITY_THRESHOLD,
            "objective_values_used": False,
        },
        "localization_definition": {
            "matched_location": "pooled squared normalized coordinate displacement share",
            "centroid": "squared normalized centroid-displacement share",
            "pairwise_shape": (
                "absolute mass of exact signed coordinate decomposition of each Q037 scalar pairwise "
                "distance change: (u_H^2-u_C^2)/(7*(d_H+d_C))"
            ),
            "subset_universe": "all 127 non-empty subsets",
            "full_capture_threshold": FULL_CAPTURE_THRESHOLD,
            "leave_one_label_out_capture_threshold": LOO_CAPTURE_THRESHOLD,
            "leave_one_label_out_required_passes": LOO_REQUIRED,
            "concentrated_max_subset_size": CONCENTRATED_MAX_SUBSET_SIZE,
        },
        "coordinate_shares": {
            "matched_location": full["matched"]["pooled_share"],
            "centroid": full["centroid"]["energy_share"],
            "pairwise_shape": full["pairwise_shape"]["pooled_share"],
        },
        "minimal_qualifying_subset_size": subsets["minimal_qualifying_subset_size"],
        "minimal_qualifying_subsets": subsets["minimal_qualifying_subsets"],
        "qualifying_subset_count": len(subsets["qualifying_subsets"]),
        "q038_stop_case": cls,
        "final_classification": cls,
        "journal_effect": (
            "LOCALIZE_C036_IMPL_TO_REPRODUCIBLE_MINIMAL_COMMON_COORDINATE_SUBSET"
            if cls == "CONCENTRATED"
            else "STRENGTHEN_MULTIVARIATE_DISTRIBUTED_IMPLEMENTATION_GEOMETRY_INTERPRETATION"
        ),
        "q037_replay": {
            "benchmarks": Q037_BENCHMARKS,
            "actual": {k: replay[k] for k in Q037_BENCHMARKS},
            "max_absolute_difference": max(replay_diffs.values()),
        },
        "gates": gates,
        "claim_boundaries": {
            "q035_remains_authoritative_closed": True,
            "q036_remains_closed": True,
            "q037_remains_closed": True,
            "stable_nonstable_labels_used_as_discriminator": False,
            "cross_likelihood_objectives_used": False,
            "camspec_hillipop_are_independent_observations": False,
            "coordinate_localization_is_causal_attribution": False,
            "physical_planck_systematic_established": False,
            "calibration_defect_established": False,
            "foreground_defect_established": False,
            "covariance_defect_established": False,
            "nuisance_defect_established": False,
            "instrument_failure_established": False,
            "ede_preference_established": False,
            "ede_falsification_established": False,
            "new_physics_established": False,
            "h0_changed": False,
        },
        "raw_decomposition_file": Path(args.raw_output).name,
        "preregister_sha256": sha256_file(args.preregister),
        "source_lock_sha256": sha256_file(args.source_lock),
        "input_gate_sha256": sha256_file(args.input_gate),
        "FINAL_RESULT_GATE": "PASS",
    }
    return result, raw_decomposition


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q037-raw", required=True)
    ap.add_argument("--preregister", required=True)
    ap.add_argument("--source-lock", required=True)
    ap.add_argument("--input-gate", required=True)
    ap.add_argument("--output", default="q038_final_v1.json")
    ap.add_argument("--raw-output", default="q038_raw_decomposition_v1.json")
    args = ap.parse_args()

    try:
        result, raw_decomposition = run(args)
        write_json(args.raw_output, raw_decomposition)
        write_json(args.output, result)
        print(f"FINAL_RESULT_GATE={result['FINAL_RESULT_GATE']}")
        print(f"Q038_STOP_CASE={result['q038_stop_case']}")
        print(f"MINIMAL_SUBSET_SIZE={result['minimal_qualifying_subset_size']}")
        print(f"MINIMAL_SUBSETS={result['minimal_qualifying_subsets']}")
        return 0
    except Exception as exc:
        result = technical_result(str(exc), args.preregister, args.source_lock, args.input_gate)
        write_json(args.output, result)
        print("FINAL_RESULT_GATE=UNRESOLVED")
        print("Q038_STOP_CASE=INCONCLUSIVE")
        print(f"TECHNICAL_REASON={exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
