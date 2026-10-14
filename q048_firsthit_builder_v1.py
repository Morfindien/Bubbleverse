#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import argparse, hashlib, json, math, sys, platform

HERE=Path(__file__).resolve().parent
CONFIG=HERE/"q048_firsthit_builder_config_v1.json"

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def load():
    c=json.loads(CONFIG.read_text())
    for v in c["inputs"].values():
        if sha(v["path"])!=v["sha256"]: raise RuntimeError("HASH_MISMATCH "+v["path"])
    root=Path(c["source_root"])
    sys.path.insert(0,str(root))
    import q047_math_v1 as m
    import q048_prefix_v1 as p
    import q047_precursor_check_v1 as pre
    captured=p.validate_config(json.loads(Path(c["inputs"]["captured_config"]["path"]).read_bytes()))
    p2=json.loads(Path(c["inputs"]["p2p4_result"]["path"]).read_text())
    m19=json.loads(Path(c["inputs"]["math019_result"]["path"]).read_text())
    return c,m,p,pre,captured,p2,m19

def frac_interval(m,obj):
    return m.I(F(obj["lo"]),F(obj["hi"]))

def pair(x):
    return {"lo":str(x.lo),"hi":str(x.hi),"display_lo":float(x.lo),"display_hi":float(x.hi)}

def dynamic_helium_boundary(m,t,h,H,z=1600):
    q=m.I(F(1,1_000_000)); f=t["fHe"]; T0=t["T0"]; n0=t["nH0"]
    Tg=T0*(1+z); n=n0*((1+z)**3)/10**6; Hs=H*m.C["c"]/m.C["Mpc"]
    s0=4*m.const("2.414194e15")*Tg*m.root(Tg)/n
    s=s0*m.ex(-m.const("285325")/Tg)
    y2s=m.ex(m.const("46090")/Tg)/s0
    y2p=3*m.ex(m.const("39101")/Tg)/s0
    neutral=m.I(1)-h
    eta=m.const("9.15776e22")*Hs/n/neutral
    g=m.const("1.976e6")/(1-m.ex(-m.const("6989")/Tg))
    for aa,bb in [("6.03e6","19754"),("1.06e8","21539"),("2.18e6","28496"),
                  ("3.37e7","29224"),("1.04e6","32414"),("1.51e7","32781")]:
        g=g+m.const(aa)/(m.ex(m.const(bb)/Tg)-1)
    tau=m.const("4.277e-8")*n/Hs*(f-q)
    tauc=g*tau/(4*m.C["pi"]**2)/eta
    enh=m.root(1+m.C["pi"]**2*tauc)+m.const("7.74")*tauc/(1+70*tauc)
    A=1-m.ex(-m.const("1.023e-7")*tau)
    B=m.ex(-m.const("6.14e13")/eta)
    C=m.const("0.964525")*m.ex(m.const("2947")/Tg)
    # Positive algebraic rewrite of source escape probability.
    pesc=(enh*(1-A*B)+A*C)/tau
    K=(m.const("50.94")*y2s+m.const("1.7989e9")*y2p*pesc)/Hs
    D=(f-q)*s-q*(q+h)
    qu=K*D
    return {"Tgamma":Tg,"s":s,"D":D,"K":K,"q_u":qu,"neutral":neutral}

def native_phase5_q(row):
    s=row["thermal_starts"][5]
    assert s["phase"]==5 and s["He_index"]==1 and s["mz"]=="-0x1.9p+10"
    f=F.from_float(float.fromhex(s["constants"]["fHe_HyRec"]))
    xhe=F.from_float(float.fromhex(s["y"][s["He_index"]]))
    return f*xhe

def main():
    c,m,p,pre,captured,p2,m19=load()
    eps=F(1,1_000_000)
    cases={}
    obstruction=False
    for name,row in captured["cases"].items():
        t=p.parameters(row)
        hentry=p2["cases"][name]["H_entry"]["q"]
        hentry_lo=F(hentry["lo"]); hentry_hi=F(hentry["hi"])
        qdom=p2["cases"][name]["frec_entry_state_enclosure"]["q_domain"]
        qlo,qhi=F(qdom["lo"]),F(qdom["hi"])
        h=frac_interval(m,p2["cases"][name]["frec_entry_state_enclosure"]["h_HII"])

        # Exact base-background H at a=1/1601 from captured finite-node source.
        base=dict(t); base["ede"]=None
        baseH=pre.background(m.I(F(1,1601)),base)["H"]

        if t["ede"] is None:
            H=baseH
            energy_cap=None
        else:
            eco=[F(v["boundary_E_upper_exact"]) for v in m19["second_discriminator"]["ede_constructions"].values()
                 if v["case"]==name]
            Emax=max(eco)
            floor=t["ede"]["B"]*m.const("3.968e-8")
            H2=baseH**2 + m.I(F(0),(Emax+floor.hi)/3)
            H=m.sqrt_i(H2)
            energy_cap=str(Emax)

        rate=dynamic_helium_boundary(m,t,h,H)
        nativeq=native_phase5_q(row)
        native_margin=eps-nativeq
        hentry_pass=hentry_lo>eps
        qdomain_spans=(qlo<=eps<=qhi)
        boundary_direction=(rate["D"].hi<0 and rate["K"].lo>0 and rate["q_u"].hi<0)
        nu=-rate["q_u"].hi if boundary_direction else F(0)
        obstruction = obstruction or qdomain_spans

        cases[name]={
            "H_entry":{"q_lo":str(hentry_lo),"q_hi":str(hentry_hi),"q_lo_display":float(hentry_lo),
                       "q_hi_display":float(hentry_hi),"E1_entry_above_epsilon":hentry_pass},
            "frec_source_real_q_domain":{"lo":str(qlo),"hi":str(qhi),"contains_epsilon":qdomain_spans,
                "interpretation":"Serialized admitted domain only; not a correlated trajectory endpoint."},
            "native_phase5_diagnostic":{"q_exact":str(nativeq),"q_display":float(nativeq),
                "epsilon_minus_q_exact":str(native_margin),"epsilon_minus_q_display":float(native_margin),
                "below_exact_epsilon":nativeq<eps,
                "source_real_event_evidence":False,
                "reason":"No P6/source-native trajectory error enclosure is available at the ~1e-12 margin."},
            "frec_boundary_transversality_at_exact_epsilon":{
                "h_HII":pair(h),"H_Mpc_inverse":pair(H),"ede_boundary_energy_upper":energy_cap,
                "D":pair(rate["D"]),"K":pair(rate["K"]),"q_u":pair(rate["q_u"]),
                "nu_lower_exact":str(nu),"nu_lower_display":float(nu),
                "strict_downward":boundary_direction,
                "scope":"Instantaneous q=epsilon boundary tube at z=1600; not an E2 bracket."
            }
        }

    all_entry=all(v["H_entry"]["E1_entry_above_epsilon"] for v in cases.values())
    all_down=all(v["frec_boundary_transversality_at_exact_epsilon"]["strict_downward"] for v in cases.values())
    all_native_below=all(v["native_phase5_diagnostic"]["below_exact_epsilon"] for v in cases.values())
    all_domains_span=all(v["frec_source_real_q_domain"]["contains_epsilon"] for v in cases.values())

    if all_entry and all_down and all_domains_span:
        status="BOUNDED_LOCALIZATION_OBSTRUCTION"
        blocker="SOURCE_REAL_FREC_Q_ENDPOINT_CORRELATION_NOT_SERIALIZED"
        stop=("The admitted source-real frec q enclosure is [0,qmax] in every case and contains epsilon. "
              "Native phase samples lie below epsilon but lack a source-real/P6 error enclosure. "
              "Therefore E2 and full E1-firstness cannot be certified from the serialized state. "
              "Dynamic frec integration would require a sign-separated correlated q/h/w initial endpoint that is not present.")
    else:
        status="UNEXPECTED_GATE_FAILURE"
        blocker="PREBOUNDARY_REQUIRED_GATE_FAILED"
        stop="One or more prerequisite boundary checks did not match the frozen expected discriminator."

    result={
        "schema":"Q048_FIRSTHIT_BUILDER_RESULT_V1",
        "q":"Q048","task_id":c["task_id"],"result_id":c["result_id"],"program_id":c["program_id"],
        "program_registry_status":c["program_registry_status"],
        "question_sha256":c["identity"]["question_sha256"],
        "source_commit":c["identity"]["source_commit"],
        "captured_config_sha256":c["identity"]["captured_config_sha256"],
        "prepared_config_utc":c["prepared_utc"],
        "executed_utc":datetime.now(timezone.utc).isoformat(),
        "execution_status":"COMPLETE",
        "result_validation_status":"PROVISIONAL",
        "scientific_outcome":"INCONCLUSIVE_FOR_EVENT_LOCALIZATION",
        "task_terminal_status":status,
        "cases":cases,
        "aggregate":{
            "all_H_entry_q_above_epsilon":all_entry,
            "all_frec_source_real_q_domains_span_epsilon":all_domains_span,
            "all_native_phase5_q_below_exact_epsilon":all_native_below,
            "all_boundary_q_u_strictly_negative_at_epsilon":all_down,
            "E1_complete":False,
            "E2_complete":False,
            "E3_bracket_complete":False,
            "new_boundary_direction_component":"PASS" if all_down else "FAIL"
        },
        "first_material_blocker":{"id":blocker,"detail":stop},
        "minimum_resolving_evidence":[
            "A correlation-preserving conditional-source-real H-phase q endpoint enclosure at a=1/1601, or an earlier serialized E2 bracket, that separates q from epsilon.",
            "A connected accepted-cell record sufficient for E1 earlier-root exclusion.",
            "If the recovered boundary has q_lower>epsilon, continue dynamic frec q/h/w only within the MATH019 admitted z=1600→1599 cell; if q_upper<epsilon, localize the bracket in H mode; if it still straddles epsilon, refine the H endpoint/order enclosure."
        ],
        "native_P6":"UNRESOLVED",
        "post_event_histories":"NOT_EXECUTED",
        "complete_xe_tau":"NOT_COMPUTED",
        "q_complete":False,
        "return_route":"RESULT INGESTION & ROUTING ENGINE",
        "python":platform.python_version(),
        "notes":[
            "No native phase sign was promoted to a source-real event claim.",
            "No dynamic frec hydrogen integration was started after the source-real q endpoint failed sign separation.",
            "No P3, Math015-019, V9, likelihood, refit, capture or post-event history was rerun."
        ]
    }
    out=HERE/"q048_firsthit_builder_result_v1.json"
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps({"status":status,"blocker":blocker,
                      "boundary_nu":{k:v["frec_boundary_transversality_at_exact_epsilon"]["nu_lower_display"] for k,v in cases.items()}},
                     indent=2))

if __name__=="__main__": main()
