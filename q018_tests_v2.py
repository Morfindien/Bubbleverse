#!/usr/bin/env python3
import argparse,json,math
from pathlib import Path
import yaml
Q="Q018"; RUN="Q018-PLANCK-LIKELIHOOD-BRIDGE-V2"
BR=("full_native","full_likelihood_only","shared3_only","foreground6_only")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",required=True); ap.add_argument("--merged",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); c=yaml.safe_load(Path(a.config).read_text()); d=json.loads(Path(a.merged).read_text())
    g={}
    g["Q_IDENTITY_GATE"]=d.get("q")==Q and d.get("run_id")==RUN
    g["MODEL_IDENTITY_GATE"]=c["model"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97" and int(c["model"]["n_scf"])==3
    g["ENDPOINT_IDENTITY_GATE"]=float(c["endpoints"]["free_h0"])==67.988328967159 and float(c["endpoints"]["fixed_h0"])==71.5
    g["JOB_COMPLETENESS_GATE"]=all(b in d.get("computed_bridge_penalties",{}) for b in BR)
    spreads=d.get("stability",{})
    # Replication gate: at least two complete starts for every bridge/endpoint and finite spread.
    g["MULTISTART_REPLICATION_GATE"]=all(
        int(spreads.get(f"{b}:{e}",{}).get("complete",0))>=2
        for b in BR for e in ("reference_free_h0","fixed_h0_71p5"))
    p=d.get("computed_bridge_penalties",{})
    g["FINITE_RESULT_GATE"]=all(math.isfinite(float(v)) for v in p.values()) if p else False
    # Reproduce the Q017 native full-MF penalty before interpreting bridge deltas.
    tol=0.50
    g["Q017_NATIVE_REFERENCE_GATE"]=abs(float(p.get("full_native",1e99))-float(c["references"]["q017_full_mf_penalty"]))<=tol if p else False
    g["NO_INVALID_ADDITIVITY_GATE"]=d.get("interpretation_rules",{}).get("lock_surfaces_are_not_additive_components") is True
    mandatory=list(g)
    final=all(g[k] for k in mandatory)
    result={"q":Q,"run_id":RUN,"stage":"TESTS","gates":g,"mandatory":mandatory,
            "final_result_gate":"PASS" if final else "FAIL",
            "scientific_result_available":bool(final),
            "classification_rule":{
                "single_component":"Only if one controlled bridge change reproducibly accounts for >=0.75 of the architecture-gap magnitude while the remaining valid diagnostics are subdominant and the native-reference gate passes.",
                "coupled_components":"Use when >=2 controlled changes are required or interaction/architecture residual remains material.",
                "indeterminate":"Use when native reference cannot be reproduced or the architecture residual cannot be separated with certifiable adapters."
            }}
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    return 0 if final else 2
if __name__=="__main__": raise SystemExit(main())
