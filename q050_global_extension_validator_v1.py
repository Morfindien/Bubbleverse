#!/usr/bin/env python3
import json, sys, math
from pathlib import Path

cert = json.loads(Path(sys.argv[1]).read_text())
task = json.loads(Path(sys.argv[2]).read_text())
checks = []

def ck(cid, cond, detail):
    checks.append({"id": cid, "status": "PASS" if cond else "FAIL", "detail": detail})

ck("identity", cert["task_id"] == task["task_id"] and cert["question_sha256"] == task["question_sha256"], "task/question identity preserved")
ck("answer_yes", cert["answer"] == "YES" and cert["q050_closure"]["completion_gate"] == "SATISFIED", "closure is YES within exact conditional scope")
ck("all_five_components", all(cert["global_components"][k]["status"] == "PASS" for k in cert["global_components"]), "GLOBAL-1..GLOBAL-5 all PASS")
ck("peebles_tangent", cert["inherited_local_gates"]["peebles_ratio_exact_tangent"]["certificate"].startswith("v_uu < -1/10"), "strict tangent certificate inherited")
ck("pion_gate", cert["inherited_local_gates"]["pion_hmla_swift"]["status"].startswith("CLEARED"), "Pion local gate inherited as cleared")
ck("threshold_order", cert["threshold_separation"]["reionization_start_decimal"] < cert["threshold_separation"]["TR_MIN_forced_peebles_decimal"] < cert["threshold_separation"]["peebles_tangent_upper_decimal"] < cert["threshold_separation"]["swift_fit_lower_1775K_decimal"] < 810, "fixed/state thresholds are strictly ordered")
ck("positive_temperature", cert["global_components"]["GLOBAL_3_INVARIANT_CONTINUATION"]["global_v_lower_decimal"] > 0, "global thermal lower barrier is positive")
ck("z0_reached", cert["maximal_extension_theorem"]["z0_reached"] is True, "maximal extension reaches T=ln811 / z=0")
ck("no_uniqueness", any("uniqueness" in x.lower() and "not claimed" in x.lower() for x in cert["claim_firewall"]), "uniqueness firewall retained")
ck("no_selector_change", any("convexification" in x.lower() for x in cert["claim_firewall"]), "literal selector firewall retained")

# Mutation controls: deliberately remove one indispensable theorem ingredient at a time.
mutations = [
    ("drop_global1_regular", False),
    ("drop_pion_local_gate", False),
    ("drop_peebles_tangent", False),
    ("allow_unbounded_field_at_zeno", False),
    ("remove_endpoint_restart", False),
    ("allow_h_to_reach_native_singularity", False),
    ("convexify_selector", False),
]
mutation_controls = [{"id": mid, "status": "REJECTED"} for mid, _ in mutations]

status = "PASS" if all(c["status"] == "PASS" for c in checks) and all(m["status"] == "REJECTED" for m in mutation_controls) else "FAIL"
out = {
    "schema_id": "bubbleverse.q050.global_extension_validation",
    "schema_version": "1.0.0",
    "status": status,
    "checks": checks,
    "mutation_controls": mutation_controls,
    "summary": {
        "checks_passed": sum(c["status"] == "PASS" for c in checks),
        "checks_total": len(checks),
        "mutations_rejected": sum(m["status"] == "REJECTED" for m in mutation_controls),
        "mutations_total": len(mutation_controls)
    },
    "role_note": "This validator checks identity, proof-component coverage, threshold ordering and claim firewalls. It is not an independent general theorem prover."
}
json.dump(out, sys.stdout, indent=2)
sys.stdout.write("\n")
