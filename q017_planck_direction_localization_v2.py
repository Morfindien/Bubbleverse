#!/usr/bin/env python3
"""
Bubbleverse Q017 V2 execution wrapper.

V2 is a technical repair of V1's static-gate/orchestration layer only. The
scientific/numerical implementation is reused byte-for-byte from
q017_planck_direction_localization_v1.py. V2 changes run/result identity while
preserving Q017, Q016 endpoint locks, likelihood, nuisance model, tolerances,
classification rules and computational semantics.
"""
from __future__ import annotations
import q017_planck_direction_localization_v1 as impl

impl.RUN = "Q017-PLANCK-DIRECTION-LOCALIZATION-V2"
impl.RESULT = "R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-002"

if __name__ == "__main__":
    raise SystemExit(impl.main())
