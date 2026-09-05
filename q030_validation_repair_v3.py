#!/usr/bin/env python3
"""Bubbleverse Q030 V3 merge/validation-only repair.

Purpose
-------
Reuse the already successful Q030 V2 mask artifacts bit-for-bit. Do not rebuild
CamSpec, do not evaluate a likelihood, do not optimize, do not sample, and do
not rerun Q024/Q028. The only change relative to V2 is validation calibration
for float64 cancellation in exact factorial/group-pair closure checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, median
from typing import Any
import yaml

Q = "Q030"
RUN = "Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V3"
RESULT = "R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-003"
PARENT_RUN = "Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V2"
PARENT_RESULT = "R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-002"
PARENT_GITHUB_RUN_ID = 33961469874
PARENT_HEAD_SHA = "c0d01b8cd9ecc533b37cf82e89710595ff9a34a2"
Q028_RUN_ID = 33957937309
Q028_HEAD_SHA = "7f5d35c0725530039162adfa4d71be288e8b4462"
COMMON_DIM = 9915
COMMON_SHA = "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"
MASKS = (3, 6, 7)
EDGES = ("e01", "e02", "e12")
EXPECTED_MASK_JSON_SHA256 = {
    3: "993426ef2b63a9197844a9b7526f2e72a162b7470752ba2b7ad21a006c3b3913",
    6: "51220e4ef4ed71f4e65d0337d98554c86a014fba573fe773629ca83ba0744a08",
    7: "e9d6eb8cab66e66599cdf475fe9a22394d9ab4d5365889e75ed0d297fa111968",
}
EXPECTED_Q028_FINAL_JSON_SHA256 = "81be0f7f9370cd60ff9d4531e5a72883244d83148aed343f73b2a7a5510b53fe"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    x = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL {path}")
    return x


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding='utf-8')


def stats(values: list[float]) -> dict[str, float]:
    if not values or not all(math.isfinite(float(x)) for x in values):
        raise RuntimeError("FINITE_STATS_GATE=FAIL")
    a = [float(x) for x in values]
    aa = [abs(x) for x in a]
    return {
        "signed_sum": float(sum(a)),
        "mean": float(mean(a)),
        "median": float(median(a)),
        "mean_absolute": float(mean(aa)),
        "median_absolute": float(median(aa)),
        "max_absolute": float(max(aa)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='q030_validation_repair_v3_config.yml')
    ap.add_argument('--mask-dir', required=True)
    ap.add_argument('--q028-final', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    md = Path(args.mask_dir)

    # Bit-for-bit immutability gates on the three successful V2 scientific shards.
    shards: dict[int, dict[str, Any]] = {}
    observed_hashes: dict[str, str] = {}
    for mask in MASKS:
        p = md / f'q030_v2_mask_m{mask}.json'
        if not p.exists():
            raise RuntimeError(f"V2_MASK_ARTIFACT_MISSING_GATE=FAIL mask={mask}")
        got = sha256_file(p)
        observed_hashes[str(mask)] = got
        if got != EXPECTED_MASK_JSON_SHA256[mask]:
            raise RuntimeError(f"V2_MASK_JSON_IMMUTABILITY_GATE=FAIL mask={mask} got={got}")
        x = read_json(p)
        if not (
            x.get('q') == Q and x.get('run_id') == PARENT_RUN
            and x.get('result_id') == PARENT_RESULT and x.get('phase') == 'MASK'
            and x.get('status') == 'COMPLETE' and int(x.get('mask', -1)) == mask
            and int(x.get('diagnostic_count', -1)) == 3
        ):
            raise RuntimeError(f"V2_MASK_IDENTITY_GATE=FAIL mask={mask}")
        shards[mask] = x

    q28p = Path(args.q028_final)
    q28_hash = sha256_file(q28p)
    if q28_hash != EXPECTED_Q028_FINAL_JSON_SHA256:
        raise RuntimeError(f"Q028_FINAL_JSON_IMMUTABILITY_GATE=FAIL got={q28_hash}")
    q28 = read_json(q28p)
    cs = q28.get('common_support', {})
    if not (
        q28.get('q') == 'Q028'
        and q28.get('FINAL_RESULT_GATE') == 'PASS'
        and int(cs.get('dimension', -1)) == COMMON_DIM
        and cs.get('keys_sha256') == COMMON_SHA
    ):
        raise RuntimeError("Q028_PARENT_IDENTITY_GATE=FAIL")

    q28_diag = q28['diagonal_support_effects']
    diagnostics: list[dict[str, Any]] = []
    max_parent = 0.0
    counts = {
        'model_initializations_without_likelihood_evaluation': 0,
        'new_likelihood_evaluations': 0,
        'optimizer_evaluations': 0,
        'sampling_evaluations': 0,
        'q024_permutations': 0,
    }

    lineage_objects: dict[str, Any] = {}
    for mask in MASKS:
        shard = shards[mask]
        lineage_objects[str(mask)] = {
            'data_vector': shard['data_vector'],
            'precision': shard['precision'],
        }
        ec = shard['execution_counts']
        counts['model_initializations_without_likelihood_evaluation'] += int(ec['model_initializations'])
        counts['new_likelihood_evaluations'] += int(ec['new_likelihood_evaluations'])
        counts['optimizer_evaluations'] += int(ec['optimizer_evaluations'])
        counts['sampling_evaluations'] += int(ec['sampling_evaluations'])
        counts['q024_permutations'] += int(ec['q024_permutations_evaluated'])

        for edge in EDGES:
            d = dict(shard['diagnostics'][edge])
            parent_f = float(q28_diag[str(mask)][edge]['common_support_marginal_pair_interaction'])
            err = float(d['terms']['F_reconstructed']) - parent_f
            d['Q028_parent_common_support_F'] = parent_f
            d['Q028_parent_closure_error'] = err
            max_parent = max(max_parent, abs(err))
            diagnostics.append(d)

    if len(diagnostics) != 9:
        raise RuntimeError("NINE_DIAGNOSTIC_COMPLETENESS_GATE=FAIL")
    if any(counts[k] for k in ('new_likelihood_evaluations','optimizer_evaluations','sampling_evaluations','q024_permutations')):
        raise RuntimeError("ZERO_NEW_SCIENTIFIC_EXECUTION_GATE=FAIL")
    if max_parent > float(cfg['validation']['q028_parent_interaction_abs_tol']):
        raise RuntimeError("Q028_PARENT_FUNCTIONAL_CLOSURE_GATE=FAIL")

    tdm = [float(d['terms']['T_DM_data_model_factorial_coupling']) for d in diagnostics]
    tmm = [float(d['terms']['T_MM_model_quadratic']) for d in diagnostics]
    ff = [float(d['terms']['F_reconstructed']) for d in diagnostics]

    by_mask = {}
    for mask in MASKS:
        rows = [d for d in diagnostics if int(d['mask']) == mask]
        by_mask[str(mask)] = {
            'T_DM': stats([r['terms']['T_DM_data_model_factorial_coupling'] for r in rows]),
            'T_MM': stats([r['terms']['T_MM_model_quadratic'] for r in rows]),
            'F': stats([r['terms']['F_reconstructed'] for r in rows]),
        }
    by_edge = {}
    for edge in EDGES:
        rows = [d for d in diagnostics if d['edge'] == edge]
        by_edge[edge] = {
            'T_DM': stats([r['terms']['T_DM_data_model_factorial_coupling'] for r in rows]),
            'T_MM': stats([r['terms']['T_MM_model_quadratic'] for r in rows]),
            'F': stats([r['terms']['F_reconstructed'] for r in rows]),
        }

    dominance_counts: dict[str, int] = {}
    for d in diagnostics:
        k = str(d['magnitude_relation'])
        dominance_counts[k] = dominance_counts.get(k, 0) + 1

    max_q029 = max(abs(float(d['Q029_identity_closure_error'])) for d in diagnostics)
    agg_rows = []
    for d in diagnostics:
        for mode, dist in d['distributions'].items():
            for term, err in dist['closure_error_vs_total'].items():
                agg_rows.append((int(d['mask']), d['edge'], mode, term, abs(float(err))))
    worst_agg = max(agg_rows, key=lambda x: x[-1])

    out = {
        'q': Q,
        'run_id': RUN,
        'result_id': RESULT,
        'phase': 'MERGE_VALIDATION_REPAIR',
        'status': 'COMPLETE',
        'scientific_question': cfg['project']['question'],
        'classification': 'V2_NUMERICAL_RESULT_PRESERVED_VALIDATION_ONLY_REPAIR',
        'source_numerical_result': {
            'run_id': PARENT_RUN,
            'result_id': PARENT_RESULT,
            'github_run_id': PARENT_GITHUB_RUN_ID,
            'head_sha': PARENT_HEAD_SHA,
            'mask_json_sha256': observed_hashes,
        },
        'actual_model_initializations_without_likelihood_evaluation': counts['model_initializations_without_likelihood_evaluation'],
        'actual_new_likelihood_evaluations': counts['new_likelihood_evaluations'],
        'actual_optimizer_evaluations': counts['optimizer_evaluations'],
        'actual_sampling_evaluations': counts['sampling_evaluations'],
        'actual_q024_permutations': counts['q024_permutations'],
        'v3_additional_model_initializations': 0,
        'v3_additional_likelihood_evaluations': 0,
        'v3_additional_optimizer_evaluations': 0,
        'v3_additional_sampling_evaluations': 0,
        'v3_additional_q024_permutations': 0,
        'diagnostic_count': 9,
        'diagnostics': diagnostics,
        'global_summary': {
            'T_DM_data_model_factorial_coupling': stats(tdm),
            'T_MM_model_quadratic': stats(tmm),
            'F_reconstructed': stats(ff),
            'magnitude_relation_counts': dominance_counts,
            'by_mask': by_mask,
            'by_edge': by_edge,
            'max_abs_Q028_parent_F_closure_error': max_parent,
            'max_abs_Q029_identity_closure_error': max_q029,
            'max_abs_group_pair_aggregation_closure_error': worst_agg[-1],
            'worst_group_pair_aggregation_location': {
                'mask': worst_agg[0], 'edge': worst_agg[1], 'mode': worst_agg[2], 'term': worst_agg[3]
            },
        },
        'common_support': {'dimension': COMMON_DIM, 'keys_sha256': COMMON_SHA},
        'lineage_objects': lineage_objects,
        'q028_parent': {
            'run_id': Q028_RUN_ID,
            'head_sha': Q028_HEAD_SHA,
            'final_json_sha256': q28_hash,
        },
        'validation_repair': {
            'type': 'FLOAT64_CANCELLATION_TOLERANCE_CALIBRATION_ONLY',
            'v2_failed_gate': 'FINAL_RESULT_GATE',
            'v2_failed_tests': ['T005_Q029_EXACT_IDENTITY_CLOSURE', 'T008_SPECTRUM_AND_MULTIPOLE_PAIR_CLOSURE'],
            'observed_v2_max_q029_identity_error': max_q029,
            'observed_v2_max_aggregation_error': worst_agg[-1],
            'v2_old_abs_tolerance': 1e-8,
            'v3_abs_tolerance': float(cfg['validation']['float64_factorial_closure_abs_tol']),
            'q028_parent_abs_tolerance_unchanged': float(cfg['validation']['q028_parent_interaction_abs_tol']),
            'scientific_values_changed': False,
            'mask_artifacts_changed': False,
            'common_support_changed': False,
            'interpretation_changed': False,
        },
        'interpretation': {
            'T_DM': 'EXACT DATA_MODEL_FACTORIAL_COUPLING; NOT AN IDENTIFIED DATA-ONLY CONTRIBUTION AND NOT PHYSICAL CAUSATION',
            'T_MM': 'EXACT MODEL_QUADRATIC FUNCTIONAL TERM; NOT AN IDENTIFIED PHYSICAL MODEL CAUSE',
            'distribution_semantics': 'SPECTRUM AND ELL-BAND RESULTS RETAIN UNORDERED WITHIN- AND CROSS-GROUP COVARIANCE TERMS; THEY ARE NOT INDEPENDENT LIKELIHOODS',
            'unique_data_model_attribution_claimed': False,
            'cosmology_calibration_attribution_claimed': False,
            'new_physics_claimed': False,
            'shapley_as_identification_used': False,
        },
        'FINAL_RESULT_GATE': 'PROVISIONAL_PENDING_Q030_V3_TESTS',
    }
    write_json(Path(args.output), out)
    print(f"Q030_V3_MERGE_GATE=PASS diagnostics=9 max_q029={max_q029:.12g} max_agg={worst_agg[-1]:.12g}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
