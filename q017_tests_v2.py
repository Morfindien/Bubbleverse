#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import yaml

Q="Q017"
RUN="Q017-PLANCK-DIRECTION-LOCALIZATION-V2"
RESULT="R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-002"

def write(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def git_blob(path):
    p=subprocess.run(["git","hash-object",path],text=True,capture_output=True)
    return p.stdout.strip() if p.returncode==0 else None

def static(config, source_lock, workflow, output):
    c=yaml.safe_load(Path(config).read_text(encoding="utf-8"))
    sl=json.loads(Path(source_lock).read_text(encoding="utf-8"))
    wrapper=Path("q017_planck_direction_localization_v2.py").read_text(encoding="utf-8")
    parent_src=Path("q017_planck_direction_localization_v1.py").read_text(encoding="utf-8")
    src=wrapper+"\n"+parent_src
    setup=Path("q017_setup_v2.sh").read_text(encoding="utf-8")
    wf=Path(workflow).read_text(encoding="utf-8")
    checks={
      "Q_IDENTITY_GATE":c["project"]["q"]==Q and sl["q"]==Q,
      "RUN_IDENTITY_GATE":c["project"]["run_id"]==RUN and c["project"]["result_id"]==RESULT,
      "CASE_ID_PRESERVATION_GATE":c["project"]["case_id"]=="NOT DOCUMENTED",
      "Q016_PARENT_GATE":c["parent_q016"]["run_id"]=="Q016-MATCHED-CMB-SURFACE-V16",
      "NO_Q016_PRIMARY_RERUN_GATE":c["parent_q016"]["primary_profiles_must_not_be_rerun"] is True,
      "Q011_NOT_ENDPOINT_GATE":c["parent_q016"]["q011_vector_must_not_be_endpoint"] is True and "load_q011" not in src,
      "MODEL_GATE":c["frozen_surface"]["model"]=="ede_n3" and c["frozen_surface"]["n_scf"]==3,
      "BACKEND_GATE":c["frozen_surface"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "FULL_MF_GATE":c["frozen_surface"]["full_planck_likelihood"]=="planck_NPIPE_highl_CamSpec.TTTEEE",
      "Q014_REUSE_GATE":"q014_external_viability_v12" in src,
      "Q015_REUSE_GATE":"q015_cmb_attribution_v2" in src,
      "V1_IMPLEMENTATION_REUSE_GATE":"import q017_planck_direction_localization_v1 as impl" in wrapper,
      "V2_IDENTITY_OVERRIDE_GATE":('impl.RUN = "Q017-PLANCK-DIRECTION-LOCALIZATION-V2"' in wrapper and 'impl.RESULT = "R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-002"' in wrapper),
      "NINE_NUISANCE_GATE":len(c["nuisance"]["all"])==9,
      "TARGET_BAND_GATE":c["decomposition"]["target_band"]=={"name":"ell_600_999","min":600,"max":999},
      "COVARIANCE_FORMULA_GATE":"precision @ residual" in src and "residual * z" in src,
      "COVARIANCE_BLOCK_PAIR_GATE":"2.0 * float(rg @ (precision[np.ix_(I, J)] @ rh))" in src,
      "NO_CROSS_CHAIN_SUM_GATE":c["frozen_surface"]["no_cross_chain_chi2_sum"] is True,
      "NO_CAUSAL_CLAIM_GATE":c["decomposition"]["causal_systematic_identification"] is False,
      "IGNORE_PRIOR_FALSE_GATE":c["execution"]["ignore_prior"] is False and 'm["ignore_prior"] = False' in src,
      "SOFT_RUNTIME_GATE":int(c["execution"]["soft_stop_minutes"]) < int(c["execution"]["workflow_job_timeout_minutes"]) < int(c["execution"]["github_hard_limit_minutes"]),
      "SPLIT_BASELINE_GATE":len(c["execution"]["baseline_restarts"])>=3 and "fromJSON(needs.prepare.outputs.baseline_matrix)" in wf,
      "SPLIT_LOCK_GATE":len(c["execution"]["lock_restarts"])>=2 and "fromJSON(needs.prepare.outputs.lock_matrix)" in wf,
      "NO_FAKE_RESUME_GATE":c["execution"]["checkpointing"] is False,
      "SETUP_FULL_MF_INSTALL_GATE":(
          'cobaya-install "$component"' in setup
          and "retry_install planck_NPIPE_highl_CamSpec.TTTEEE" in setup
      ),
      "SETUP_FROZEN_CLASS_GATE":"5a131c91d657dd9a7c6364cc45b038710f8d0d97" in setup,
      "ALLOWED_CLASSIFICATIONS_GATE":set(c["allowed_terminal_classifications"])=={
        "SPECIFIC PLANCK DIRECTION LOCALIZED","BROADLY DISTRIBUTED PLANCK PENALTY","INDETERMINATE"
      },
      "SOURCE_LOCK_HEAD_GATE":sl["repository_head_at_design"]=="aa4c80a5cbadee7da3087b8dccfbc0363ec31910",
    }
    blob_checks={}
    for path,spec in sl["reused_files"].items():
        actual=git_blob(path)
        blob_checks[path]={"expected":spec["blob_sha"],"actual":actual,"pass":actual==spec["blob_sha"]}
    checks["SOURCE_BLOB_GATES"]=all(v["pass"] for v in blob_checks.values())
    status="PASS" if all(checks.values()) else "FAIL"
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"test_id":"Q017-V2-STATIC","status":status,"checks":checks,"source_blob_checks":blob_checks}
    write(output,out)
    failed={k:v for k,v in checks.items() if v is not True}
    blob_failed={k:v for k,v in blob_checks.items() if v.get("pass") is not True}
    print(json.dumps({"status":status,"failed_checks":failed,"failed_blob_checks":blob_failed},indent=2,sort_keys=True))
    if status!="PASS": raise SystemExit(2)

def final(result, output):
    d=json.loads(Path(result).read_text(encoding="utf-8"))
    allowed={"SPECIFIC PLANCK DIRECTION LOCALIZED","BROADLY DISTRIBUTED PLANCK PENALTY","INDETERMINATE"}
    gate=d.get("final_result_gate")
    checks={
      "Q_IDENTITY_GATE":d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
      "FINAL_STAGE_GATE":d.get("stage")=="FINAL",
      "CLASSIFICATION_GATE":d.get("classification") in allowed,
      "NO_Q016_INVALIDATION_GATE":d.get("q016_result_invalidated") is False,
    }
    if gate=="PASS":
        checks["SCIENTIFICALLY_USABLE_GATE"]=d.get("scientifically_usable_result") is True
    else:
        checks["UNRESOLVED_NOT_PROMOTED_GATE"]=d.get("scientifically_usable_result") is False
    status="PASS" if all(checks.values()) and gate=="PASS" else ("UNRESOLVED" if all(checks.values()) else "FAIL")
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"test_id":"Q017-V2-FINAL","status":status,"checks":checks,"final_result_gate":gate}
    write(output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    if status!="PASS": raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("static"); a.add_argument("--config",required=True); a.add_argument("--source-lock",required=True); a.add_argument("--workflow",required=True); a.add_argument("--output",required=True)
    b=sub.add_parser("final"); b.add_argument("--result",required=True); b.add_argument("--output",required=True)
    x=ap.parse_args()
    if x.cmd=="static": static(x.config,x.source_lock,x.workflow,x.output)
    else: final(x.result,x.output)
if __name__=="__main__": main()
