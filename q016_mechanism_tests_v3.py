#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import yaml

Q="Q016"; RUN="Q016-CMB-MECHANISM-V3"; RESULT="R-Q016-EDE-CMB-MECHANISM-003"

def write(p,o):Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")

def static(cfgp,outp):
    c=yaml.safe_load(Path(cfgp).read_text())
    src=Path("q016_mechanism_v3.py").read_text()
    agg=Path("q016_mechanism_aggregate_v3.py").read_text()
    wf=Path(".github/workflows/q016-cmb-mechanism-v3.yml").read_text() if Path(".github/workflows/q016-cmb-mechanism-v3.yml").exists() else Path("q016-cmb-mechanism-v3.yml").read_text()
    lock=json.loads(Path(c["parent_v16"]["lock_file"]).read_text())
    checks={
        "Q_IDENTITY_GATE":c["project"]["q"]==Q,
        "RUN_IDENTITY_GATE":c["project"]["run_id"]==RUN and c["project"]["result_id"]==RESULT,
        "PARENT_V16_GATE":lock["parent"]["run_id"]=="Q016-MATCHED-CMB-SURFACE-V16" and lock["parent"]["primary_endpoint_gate"]=="PASS",
        "NO_PRIMARY_RERUN_GATE":c["parent_v16"]["primary_profiles_must_not_be_rerun"] is True and "minimize" not in wf.lower(),
        "THREE_MATCHED_BRANCH_GATE":set(c["execution"]["matched_residual_branches"])=={"planck","spt","act"},
        "THREE_SECONDARY_BRANCH_GATE":set(c["execution"]["secondary_branches"])=={"planck","spt","act"},
        "COMMON_BAND_GATE":[(x["min"],x["max"]) for x in c["frozen_surface"]["common_bands"]]==[(600,999),(1000,1499),(1500,2000)],
        "Q015_REUSE_GATE":"q015_cmb_attribution_v2" in src,
        "Q009_REUSE_GATE":"q009_act_corrected_minima_attribution_v8" in src,
        "SIGNED_FULLCOV_GATE":"d*(cinv@d)" in src.replace(" ",""),
        "NO_CROSS_CHAIN_SUM_GATE":"cross_chain_chi2_sum_performed" in agg,
        "NO_COMBINED_SIGMA_GATE":"combined_cross_experiment_sigma_performed" in agg,
        "SHARED_COSMIC_VARIANCE_GATE":"shared_cosmic_variance_acknowledged" in agg,
        "DECISION_OWNER_GATE":"PENDING_RESULT_INGESTION" in agg,
        "STRUCTURED_UNAVAILABLE_GATE":"TECHNICALLY_UNAVAILABLE" in src and "TECHNICALLY_UNAVAILABLE" in agg,
        "FROZEN_REQUIREMENTS_BOOTSTRAP_GATE":
            "python -m pip install -r q005_hpc_v14_requirements.txt" in Path("q016_mechanism_setup_v3.sh").read_text(),
        "COBAYA_PRE_V16_GATE":
            "Q016_MECHANISM_V3_PRE_V16_FROZEN_DEPENDENCY_GATE=PASS" in Path("q016_mechanism_setup_v3.sh").read_text(),
        "PREPARE_DEPENDENCY_PREFLIGHT_GATE":
            "Q016_MECHANISM_V3_FROZEN_DEPENDENCY_BOOTSTRAP_PREFLIGHT=PASS" in wf,
        "V2_ACT_CONTEXT_REUSE_GATE":
            "9908907363" in wf and
            "sha256:0be1c794d184cf44f6ce46ccac2bda8a165c7ed3e95da9eb405f8d4b46e661a2" in wf,
        "TYPED_OUTPUT_PATH_GATE":
            'q16.base_info(v16cfg,branch,mode,0,ROOT/"_q016_mechanism_eval")' in src,
        "FORBID_STRING_OUTPUT_PATH_REGRESSION_GATE":
            'q16.base_info(v16cfg,branch,mode,0,str(ROOT/"_q016_mechanism_eval"))' not in src,
        "V2_PARTIAL_RESULT_PROVENANCE_GATE":
            "33795220733" in wf and "9908959458" in wf and
            "sha256:c502a4a769c942dddd47e24ed82fd82c17bd08dce8ec8c4156cd38ffe208d870" in wf,
        "ONLY_TWO_SECONDARY_RERUN_BRANCHES_GATE":
            "branch: [planck, spt]" in wf and "branch: [planck, spt, act]" in wf,
        "ACT_SECONDARY_BRIDGE_GATE":
            "Q016_MECHANISM_V3_V2_ACT_SECONDARY_BRIDGE_GATE=PASS" in wf,
        "FROZEN_BACKEND_GATE":c["frozen_surface"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "SPT_DATA_PIN_GATE":c["likelihoods"]["spt_full_secondary"]["data_commit"]=="2cec6e762a8c540484dd5acafc529f0035856350",
        "ACT_MFLIKE_PIN_GATE":c["likelihoods"]["act_full_secondary"]["commit"]=="4220e14efb3a995f47c9f54cb687479e558c6138",
        "V16_SETUP_BRANCH_ARGUMENT_GATE":
            'bash q016_mechanism_setup_v3.sh "${{ matrix.branch }}"' in wf,
        "COBAYA_PACKAGES_PATH_GATE":
            'COBAYA_PACKAGES_PATH: ${{ github.workspace }}/external/cobaya_packages' in wf,
        "ACT_SHARED_ASSET_SEED_GATE":
            'q016_act_data_v1/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits' in Path("q016_mechanism_setup_v3.sh").read_text(),
        "FROZEN_STACK_POST_SETUP_GATE":
            "Q016_MECHANISM_V3_POST_SETUP_FROZEN_STACK_GATE=PASS" in Path("q016_mechanism_setup_v3.sh").read_text(),
    }
    status="PASS" if all(checks.values()) else "FAIL"
    write(outp,{"q":Q,"run_id":RUN,"result_id":RESULT,"test":"STATIC","status":status,"checks":checks})
    if status!="PASS":raise SystemExit(2)

def final(resultp,cfgp,outp):
    c=yaml.safe_load(Path(cfgp).read_text());d=json.loads(Path(resultp).read_text())
    matched=d.get("matched_residual",{});secondary=d.get("secondary_mechanism",{})
    checks={
        "Q_IDENTITY_GATE":d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
        "MATCHED_COMPLETENESS_GATE":set(matched)=={"planck","spt","act"} and all(matched[x].get("status")=="PASS" for x in matched),
        "SECONDARY_STATUS_GATE":set(secondary)=={"planck","spt","act"} and all(secondary[x].get("status") in {"PASS","TECHNICALLY_UNAVAILABLE"} for x in secondary),
        "COVARIANCE_CLOSURE_GATE":all(x.get("pass") for x in d.get("covariance_closure",{}).values()) and len(d.get("covariance_closure",{}))==3,
        "RESIDUAL_VECTOR_GATE":all(len(matched[x]["delta"]["residual_vector_fixed_minus_free"])>0 for x in matched),
        "OBSERVABLE_GATE":all(set(matched[x]["delta"]["by_observable_signed_fullcov"]).issuperset({"TT","TE","EE"}) for x in matched),
        "BAND_GATE":all(set(matched[x]["delta"]["by_common_band_signed_fullcov"]).issuperset({"ell_600_999","ell_1000_1499","ell_1500_2000"}) for x in matched),
        "NO_CROSS_CHAIN_SUM_GATE":d["guards"]["cross_chain_chi2_sum_performed"] is False,
        "NO_COMBINED_SIGMA_GATE":d["guards"]["combined_cross_experiment_sigma_performed"] is False,
        "SHARED_COSMIC_VARIANCE_GATE":d["guards"]["shared_cosmic_variance_acknowledged"] is True,
        "DECISION_ROUTING_GATE":d["decision"]["owner"]=="RESULT_INGESTION_ENGINE" and d["decision"]["q016_outcome"]=="PENDING_RESULT_INGESTION",
    }
    status="PASS" if all(checks.values()) else "FAIL"
    out={
        "q":Q,"run_id":RUN,"result_id":RESULT,"test":"FINAL_MECHANISM_RESULT",
        "status":status,"checks":checks,
        "final_result_gate":status,
        "scientific_routing":"RESULT_INGESTION_FOR_Q016_A_B_C_DECISION" if status=="PASS" else "NUMERICAL_RECOVERY_ONLY_FOR_FAILED_MANDATORY_COMPONENT",
    }
    write(outp,out)
    if status!="PASS":raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("static");a.add_argument("--config",required=True);a.add_argument("--output",required=True)
    b=sub.add_parser("final");b.add_argument("--config",required=True);b.add_argument("--result",required=True);b.add_argument("--output",required=True)
    x=ap.parse_args()
    if x.cmd=="static":static(x.config,x.output)
    else:final(x.result,x.config,x.output)
if __name__=="__main__":main()
