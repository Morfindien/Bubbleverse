#!/usr/bin/env python3
TCMB_K = 2.7255
SWIFT_FIRST_T_K = 1775.0
PION_MAX = 1e-2
z_fit = SWIFT_FIRST_T_K / TCMB_K - 1.0
assert abs(z_fit - 650.2566501559347) < 1e-12
print(f"z_fit={z_fit:.15f}")
print("Pion<0.01: HMLA")
print("Pion>=0.01 and z<z_fit: HMLA")
print("Pion>=0.01 and z>=z_fit: SWIFT")
