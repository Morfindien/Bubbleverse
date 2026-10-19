"""Fresh Q048 V99 gate diagnostic scaffold for cell 980->970.

NON-AUTHORITATIVE until a numerical primitive provider has passed regression
against accepted historical cells. This script intentionally separates the five
subpredicates hidden by V98's composite NEW_CELL_UPPER_H_THERMAL:L exception.
"""
from fractions import Fraction as F
import json
from q048_full_tube_v99_reconstructed import composite_gate

CELL_Z = [980, 970]
CELL_A = ["1/981", "1/971"]
EPS = F(1, 10**6)
HMAX = F(99999, 100000)
AUTHORITATIVE_BEFORE = {"actual_count": 110, "frontier": 980}


def diagnose_branch(provider, A, Ae, saha, a, h, t, Hs, label, q):
    terms = [provider.hydrogen_barrier_term(A[i], Ae[i], saha, provider.m.I(HMAX), q) for i in range(2)]
    thermal = provider.thermal_certificate(a, h, q, t, Hs)
    admitted, checks = composite_gate(terms, thermal)
    return {
        "label": label,
        "q": str(q),
        "subpredicates": checks,
        "admitted": admitted,
        "upper_h_face_terms": provider.d.encode(terms),
        "thermal": provider.d.encode(thermal),
    }


def diagnose(provider, A, Ae, saha, a, h, t, Hs):
    branches = {
        "L": diagnose_branch(provider, A, Ae, saha, a, h, t, Hs, "L", EPS),
        "R": diagnose_branch(provider, A, Ae, saha, a, h, t, Hs, "R", F(0)),
    }
    return {
        "schema": "bubbleverse.q048.v99.gate_diagnostic.v1",
        "status": "DIAGNOSTIC_ONLY",
        "historical_replay": False,
        "scientific_acceptance": False,
        "cell_z": CELL_Z,
        "cell_a": CELL_A,
        "authoritative_state_unchanged": AUTHORITATIVE_BEFORE,
        "branches": branches,
        "v98_observed_failure": "NEW_CELL_UPPER_H_THERMAL:L",
        "note": "A numerical result is admissible only after provider regression against accepted historical cells.",
    }


def main():
    raise SystemExit(
        "V99 scaffold created. Bind a regression-validated numerical primitive provider before execution; "
        "no fabricated 980->970 values are permitted."
    )

if __name__ == "__main__":
    main()
