"""Q048 V99 reconstructed full-tube primitive layer.

STATUS: RECONSTRUCTED / NON-HISTORICAL / DIAGNOSTIC-ONLY.

This is NOT q048_full_tube_reuse_v1.py and MUST NOT be represented as the
historical V98 dependency (expected SHA256 e975c73f7e767442cb0084c61791686061be6cd045378c8fbc48ba412bd454dc,
10171 bytes). It records the recovered mathematical interface and gate semantics
needed to build a fresh V99 diagnostic implementation.

Recovered authoritative gate semantics from the V90/V98 family:
  upper_h = [hydrogen_barrier_term(A[i], Ae[i], saha, hmax, q), i=0,1]
  thermal = thermal_certificate(a, h, q, t, Hs)
  admitted iff
    upper_h[0].lo > 0 and upper_h[1].lo > 0 and
    thermal['thermal_denominator'].lo > 0 and
    thermal['beta'].lo > 0 and
    thermal['faces']['admitted'] is True.

Recovered thermal face identities from the producer-free V90 verifier:
  lower_face_inward_lower = 1 + (1 + beta.lo) * 1e-6
  upper_face_inward_margin = (1 + beta.lo) * 1e-2 - 1
for the frozen w-domain [-1e-6, 1e-2].

Important: the original numerical bodies of hydrogen_barrier_term() and
thermal_certificate() were not preserved in the currently exposed repository
bytes. Therefore this module deliberately refuses to manufacture those bodies.
The V99 diagnostic driver must bind an independently reconstructed/verified
primitive provider before any scientific value is emitted.
"""
from fractions import Fraction as F

HISTORICAL_V1 = {
    "path": "q048_full_tube_reuse_v1.py",
    "bytes": 10171,
    "sha256": "e975c73f7e767442cb0084c61791686061be6cd045378c8fbc48ba412bd454dc",
}
STATUS = "RECONSTRUCTED_NON_HISTORICAL_DIAGNOSTIC_ONLY"


def gate_subpredicates(upper_h_face_terms, thermal):
    """Expose the five V98 composite subpredicates without collapsing them."""
    return {
        "upper_h_face_0_positive": upper_h_face_terms[0].lo > 0,
        "upper_h_face_1_positive": upper_h_face_terms[1].lo > 0,
        "thermal_denominator_positive": thermal["thermal_denominator"].lo > 0,
        "thermal_beta_positive": thermal["beta"].lo > 0,
        "thermal_faces_admitted": thermal["faces"]["admitted"] is True,
    }


def composite_gate(upper_h_face_terms, thermal):
    checks = gate_subpredicates(upper_h_face_terms, thermal)
    return all(checks.values()), checks


def recovered_face_identities(beta_lo, w_lo=F(-1, 10**6), w_hi=F(1, 100)):
    """Exact identities checked by the accepted V90 verifier.

    This function is algebraic bookkeeping, not a replacement for the missing
    thermal_certificate numerical implementation.
    """
    beta_lo = F(beta_lo)
    w_lo, w_hi = F(w_lo), F(w_hi)
    return {
        "lower_face_inward_lower": 1 - (1 + beta_lo) * w_lo,
        "upper_face_inward_margin": (1 + beta_lo) * w_hi - 1,
        "admitted": (1 - (1 + beta_lo) * w_lo) > 0 and ((1 + beta_lo) * w_hi - 1) > 0,
    }


def hydrogen_barrier_term(*args, **kwargs):
    raise RuntimeError(
        "V99_MISSING_NUMERICAL_BODY: historical hydrogen_barrier_term bytes were not recovered; "
        "do not invent a scientific enclosure."
    )


def thermal_certificate(*args, **kwargs):
    raise RuntimeError(
        "V99_MISSING_NUMERICAL_BODY: historical thermal_certificate bytes were not recovered; "
        "do not invent a scientific enclosure."
    )
