#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json, subprocess, sys, hashlib

HERE=Path(__file__).resolve().parent
prog=HERE/"q048_firsthit_builder_v1.py"
r=subprocess.run([sys.executable,str(prog)],cwd=HERE,capture_output=True,text=True)
assert r.returncode==0, r.stderr
o=json.loads((HERE/"q048_firsthit_builder_result_v1.json").read_text())
assert o["task_terminal_status"]=="BOUNDED_LOCALIZATION_OBSTRUCTION"
assert o["first_material_blocker"]["id"]=="SOURCE_REAL_FREC_Q_ENDPOINT_CORRELATION_NOT_SERIALIZED"
a=o["aggregate"]
assert a["all_H_entry_q_above_epsilon"]
assert a["all_frec_source_real_q_domains_span_epsilon"]
assert a["all_native_phase5_q_below_exact_epsilon"]
assert a["all_boundary_q_u_strictly_negative_at_epsilon"]
assert not a["E1_complete"] and not a["E2_complete"] and not a["E3_bracket_complete"]
assert o["native_P6"]=="UNRESOLVED"
assert o["post_event_histories"]=="NOT_EXECUTED"
assert o["q_complete"] is False
for name,c in o["cases"].items():
    t=c["frec_boundary_transversality_at_exact_epsilon"]
    assert F(t["D"]["hi"])<0
    assert F(t["K"]["lo"])>0
    assert F(t["q_u"]["hi"])<0
    assert F(t["nu_lower_exact"])>0
    n=c["native_phase5_diagnostic"]
    assert F(n["epsilon_minus_q_exact"])>0
    assert n["source_real_event_evidence"] is False
print("PASS: 18 mandatory semantic/assertion groups")
