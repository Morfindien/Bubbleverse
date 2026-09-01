#!/usr/bin/env python3
"""Bubbleverse Q014 V6 execution wrapper.

V6 deliberately reuses the frozen V5 scientific implementation and V5 config.
Only execution mechanics are changed:
- run/provenance identity becomes V6;
- q011_shared_physics gets max_evals=960 after V5 Planck hit MAXFUN=320.
The likelihood definitions, model, priors/bounds and task matrix remain V5.
"""
from __future__ import annotations
import q014_external_viability_v5 as impl

impl.RUN_ID = "Q014-EXTERNAL-VIABILITY-V6"
impl.CODE_VERSION = "6.0-v5-science-surface-execution-repair"
impl.CONFIG_NAME = "q014_external_viability_v5_config.yml"

_original_build_info = impl.build_info

def _v6_build_info(chain, mode, start_family, restart_index, c, q011_vec, output_prefix, max_evals=None):
    if mode == "q011_shared_physics" and max_evals is None:
        max_evals = 960
    return _original_build_info(chain, mode, start_family, restart_index, c, q011_vec, output_prefix, max_evals)

impl.build_info = _v6_build_info

if __name__ == "__main__":
    raise SystemExit(impl.cli())
