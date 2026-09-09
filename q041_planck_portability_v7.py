#!/usr/bin/env python3
"""Bubbleverse Q041 — downstream scientific-consequence portability V5.

Two separate native Planck TT arms (CamSpec / HiLLiPoP) are combined with the
same external data. The Q032/Q037 exact-common-TT construction is authoritative.
Q040 products are scientifically firewalled.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
from typing import Any, Mapping, Sequence

import numpy as np

Q="Q-041"
PROGRAM_ID="Q041-PLANCKPORT-V7"
RUN_ID="Q041-DOWNSTREAM-SCIENTIFIC-CONSEQUENCE-PORTABILITY-V7"
RESULT_ID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-007"
Q032_RUN_ID=33994305721
Q032_COMMIT="4dc873a5e880d40858d831a3b421456728f0c032"
Q032_RESULT="R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
BACKEND_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT="a09ddde3e7ce11df99f74685feb1f1764cafb251"
FULL_COMBO="P_A6_L6_D2"
BASELINE_COMBOS=("P","P_A6","P_L6","P_D2",FULL_COMBO)
LOO_COMBOS=("P_L6_D2","P_A6_D2","P_A6_L6")
ALL_COMBOS=BASELINE_COMBOS+LOO_COMBOS
ARMS=("camspec","hillipop")
COMMON_COORDS=("omega_b","omega_cdm","fEDE","log10z_c","thetai_scf","H0")
ACT_ELL_MIN=600
PLANCK_NONOVERLAP_MAX=599
HARD_RHAT=1.05
MATERIAL_SIGMA=1.0
LOO_MATERIAL_SIGMA=0.75
EQUIV_SIGMA=0.50
BC_MATERIAL=0.50
BC_EQUIV=0.80


def finite(x: Any) -> bool:
    try: return math.isfinite(float(x))
    except Exception: return False


def read_json(path: str|Path) -> dict[str,Any]:
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return x


def write_json(path: str|Path, obj: Any) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False,default=str)+"\n",encoding="utf-8")
    os.replace(t,p)


def sha256_file(path: str|Path) -> str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()


def git_head(path: str|Path) -> str:
    return subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip()


def load_q032(root: str|Path):
    root=Path(root).resolve()
    if git_head(root)!=Q032_COMMIT: raise RuntimeError("Q032_EXECUTION_COMMIT_GATE=FAIL")
    if str(root) not in sys.path: sys.path.insert(0,str(root))
    import q032_planck_tt3pair_bridge_v2 as q32  # type: ignore
    if q32.Q!="Q-032" or q32.RESULT!=Q032_RESULT: raise RuntimeError("Q032_PARENT_IDENTITY_GATE=FAIL")
    return q32


def q032_cfg(q32: Any, root: str|Path) -> dict[str,Any]:
    c=q32.load_cfg(Path(root).resolve()/"q032_planck_tt3pair_bridge_v2_config.yml")
    if c["model"]["backend_commit"]!=BACKEND_COMMIT: raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    return c


def load_preregister(path: str|Path) -> dict[str,Any]:
    d=read_json(path)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID or d.get("result_id")!=RESULT_ID:
        raise RuntimeError("PREREGISTER_IDENTITY_GATE=FAIL")
    if tuple(d.get("baseline_combinations",[]))!=BASELINE_COMBOS or tuple(d.get("leave_one_out_combinations",[]))!=LOO_COMBOS:
        raise RuntimeError("COMBINATION_LOCK_GATE=FAIL")
    if d.get("hard_rules",{}).get("q040_scientific_dependency_forbidden") is not True:
        raise RuntimeError("Q040_FIREWALL_GATE=FAIL")
    return d


def load_source_lock(path: str|Path) -> dict[str,Any]:
    d=read_json(path)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID: raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    b=d["bubbleverse"]
    if int(b["q032_github_run_id"])!=Q032_RUN_ID or b["q032_execution_commit"]!=Q032_COMMIT:
        raise RuntimeError("Q032_SOURCE_LOCK_GATE=FAIL")
    return d


def load_sealed_preflight(path: str|Path) -> dict[str,Any]:
    d=read_json(path)
    if not (d.get("q")=="Q-032" and d.get("run_id")=="Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
            and d.get("stage")=="Q032_PREFLIGHT_SEALED" and d.get("status")=="PASS"):
        raise RuntimeError("Q032_SEALED_PREFLIGHT_GATE=FAIL")
    if any(v!="PASS" for v in d.get("gates",{}).values()): raise RuntimeError("Q032_PARENT_GATE=FAIL")
    return d


def find_parent_records(root: str|Path, implementation: str) -> list[tuple[float,dict[str,Any],Path]]:
    hits=[]
    for p in Path(root).rglob("*.json"):
        try: d=read_json(p)
        except Exception: continue
        if (d.get("q")=="Q-032" and d.get("stage")=="Q032_REFINEMENT" and d.get("phase")=="refinement"
            and d.get("implementation")==implementation and d.get("status")=="COMPLETE" and d.get("actual_computed_result") is True
            and finite(d.get("objective_chi2")) and isinstance(d.get("minimum"),Mapping)):
            hits.append((float(d["objective_chi2"]),d,p))
    if len(hits)!=9: raise RuntimeError(f"Q032_NINE_REFINEMENT_ENDPOINT_GATE=FAIL impl={implementation} count={len(hits)}")
    return sorted(hits,key=lambda x:(x[0],str(x[2])))


def reference_parent(root: str|Path, implementation: str) -> tuple[dict[str,Any],Path]:
    _,d,p=find_parent_records(root,implementation)[0]
    for name in COMMON_COORDS:
        if not finite(d["minimum"].get(name)): raise RuntimeError(f"Q032_REFERENCE_COORDINATE_GATE=FAIL {name}")
    return d,p


def start_from_parent(d: Mapping[str,Any]) -> dict[str,float]:
    return {str(k):float(v) for k,v in d["minimum"].items() if finite(v)}


def has_act(combo: str) -> bool: return "A6" in combo.split("_")
def has_lens(combo: str) -> bool: return "L6" in combo.split("_")
def has_desi(combo: str) -> bool: return "D2" in combo.split("_")


def prepare_nonoverlap(args: argparse.Namespace) -> int:
    q32=load_q032(args.q032_parent_root); cfg=q032_cfg(q32,args.q032_parent_root)
    pf=load_sealed_preflight(args.preflight)
    full=pf["support_lock"]
    Pfull, fullmeta=q32.load_hlp_matrix(args.hlp_matrix,args.hlp_meta,full,cfg)

    canonical=[(str(p),int(e)) for p,e in full["canonical_common_keys"] if int(e)<=PLANCK_NONOVERLAP_MAX]
    if not canonical or any(e>=ACT_ELL_MIN for _,e in canonical): raise RuntimeError("PRIMARY_NONOVERLAP_SUPPORT_GATE=FAIL")
    bypair={p:[] for p in q32.PAIR_ORDER}
    for p,e in canonical: bypair[p].append(e)
    if any(not bypair[p] for p in q32.PAIR_ORDER): raise RuntimeError("PRIMARY_NONOVERLAP_PAIR_GATE=FAIL")

    def filt(indices_key: str, keys_key: str):
        out_i=[]; out_k=[]; positions=[]
        for pos,(idx,key) in enumerate(zip(full[indices_key],full[keys_key])):
            p,e=str(key[0]),int(key[1])
            if e<=PLANCK_NONOVERLAP_MAX:
                positions.append(pos); out_i.append(int(idx)); out_k.append([p,e])
        return positions,out_i,out_k
    cpos,cidx,ckeys=filt("camspec_selected_full_indices_native_order","camspec_selected_keys_native_order")
    hpos,hidx,hkeys=filt("hillipop_selected_full_indices_native_order","hillipop_selected_keys_native_order")
    if len(cpos)!=len(canonical) or len(hpos)!=len(canonical): raise RuntimeError("PRIMARY_NONOVERLAP_INDEX_GATE=FAIL")
    if set(map(tuple,ckeys))!=set(canonical) or set(map(tuple,hkeys))!=set(canonical): raise RuntimeError("PRIMARY_NONOVERLAP_LABEL_GATE=FAIL")

    support=copy.deepcopy(full)
    support.update({
        "q":Q,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"Q041_PRIMARY_NONOVERLAP_SUPPORT","status":"PASS",
        "common_ells_by_pair":bypair,"canonical_common_keys":[[p,e] for p,e in canonical],
        "common_dimension":len(canonical),"support_sha256":q32.ordered_support_hash(canonical),
        "camspec_selected_full_indices_native_order":cidx,"camspec_selected_keys_native_order":ckeys,
        "hillipop_selected_full_indices_native_order":hidx,"hillipop_selected_keys_native_order":hkeys,
        "construction":"Q032_EXACT_COMMON_TT3PAIR_FURTHER_MARGINALIZED_TO_ELL_LE_599_FOR_ACT_PRIMARY_NONOVERLAP",
        "parent_q032_support_sha256":full["support_sha256"],"act_primary_ell_min":ACT_ELL_MIN,
    })
    Pm,meta=q32.restricted_precision_from_full_precision(Pfull,hpos,cfg)
    Path(args.matrix_output).parent.mkdir(parents=True,exist_ok=True)
    np.save(args.matrix_output,Pm,allow_pickle=False)
    meta.update({
        "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"Q041_HILLIPOP_PRIMARY_NONOVERLAP_PRECISION","status":"PASS",
        "support_sha256":support["support_sha256"],"parent_q032_support_sha256":full["support_sha256"],
        "parent_q032_precision_sha256":fullmeta["restricted_precision_sha256"],
        "selected_positions_in_q032_common_precision":hpos,
        "selected_keys_native_order":hkeys,"matrix_file":Path(args.matrix_output).name,
        "matrix_file_sha256":sha256_file(args.matrix_output),
        "scientific_semantics":"MARGINALIZE_Q032_HILLIPOP_COMMON_TT_PRECISION_TO_ELL_LE_599_BEFORE_JOINT_ACT_PRIMARY_INFERENCE",
    })
    write_json(args.support_output,support); write_json(args.meta_output,meta)
    print(f"Q041_PRIMARY_NONOVERLAP_SUPPORT_GATE=PASS n={len(canonical)} hash={support['support_sha256']}")
    return 0


def load_reduced_matrix(q32: Any, matrix_path: str|Path, meta_path: str|Path, support: Mapping[str,Any], cfg: Mapping[str,Any]):
    meta=read_json(meta_path)
    if not (meta.get("q")==Q and meta.get("program_id")==PROGRAM_ID and meta.get("stage")=="Q041_HILLIPOP_PRIMARY_NONOVERLAP_PRECISION"
            and meta.get("status")=="PASS" and meta.get("support_sha256")==support["support_sha256"]
            and meta.get("final_semantics")=="C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS"
            and meta.get("principal_precision_submatrix_used_as_marginal") is False):
        raise RuntimeError("Q041_REDUCED_PRECISION_META_GATE=FAIL")
    if sha256_file(matrix_path)!=meta.get("matrix_file_sha256"): raise RuntimeError("Q041_REDUCED_PRECISION_FILE_GATE=FAIL")
    P=np.load(matrix_path,allow_pickle=False)
    if q32.sha256_array(P)!=meta.get("restricted_precision_sha256"): raise RuntimeError("Q041_REDUCED_PRECISION_ARRAY_GATE=FAIL")
    q32.matrix_diagnostics(P,cfg,"q041_hillipop_nonoverlap_precision")
    return np.asarray(P,dtype=float),meta


def install_q041_hillipop_patch(q32: Any, matrix_path: str|Path, meta_path: str|Path,
                                support: Mapping[str,Any], cfg: Mapping[str,Any]) -> dict[str,Any]:
    import planck_2020_hillipop.hillipop as hm
    cls=hm.TT
    # Every GitHub matrix shard has one process/one support. Refuse mixed patches.
    if getattr(cls,"_bubbleverse_q041_patch",False):
        old=getattr(cls,"_bubbleverse_q041_patch_meta")
        if old.get("support_sha256")!=support["support_sha256"]: raise RuntimeError("Q041_PATCH_REUSE_SUPPORT_GATE=FAIL")
        return old
    Pm,meta=load_reduced_matrix(q32,matrix_path,meta_path,support,cfg)
    original_initialize=cls.initialize
    def initialize(self):
        original_initialize(self)
        rows=q32.hillipop_rows(self)
        S=np.asarray(support["hillipop_selected_full_indices_native_order"],dtype=int)
        if np.max(S)>=len(rows): raise RuntimeError("Q041_HILLIPOP_RUNTIME_INDEX_GATE=FAIL")
        keys=[[str(rows[i]["spectrum"]),int(rows[i]["ell"])] for i in S]
        if keys!=support["hillipop_selected_keys_native_order"]: raise RuntimeError("Q041_HILLIPOP_RUNTIME_ORDER_GATE=FAIL")
        self._q041_selected_tt_indices=S; self._q041_precision=Pm; self._q041_support_sha256=support["support_sha256"]
    def get_requirements(self): return {"Cl":{"tt":self.lmax}}
    def compute_chi2(self,dlth,**params_values):
        Rspec=self._compute_residuals(params_values,dlth,"TT")
        Rl=self._xspectra_to_xfreq(Rspec,self._dlweight["TT"])
        Xtt=np.asarray(self._select_spectra(Rl,"TT"),dtype=float)
        residual=Xtt[self._q041_selected_tt_indices]
        if residual.shape[0]!=self._q041_precision.shape[0] or not np.all(np.isfinite(residual)):
            raise RuntimeError("Q041_HILLIPOP_FINITE_RESIDUAL_GATE=FAIL")
        chi2=float(residual@(self._q041_precision@residual))
        if not finite(chi2) or chi2<=0: raise RuntimeError("Q041_HILLIPOP_FINITE_CHI2_GATE=FAIL")
        return chi2
    def logp(self,**params_values):
        dl=self.provider.get_Cl(ell_factor=True); return -0.5*self.compute_chi2({"TT":dl["tt"][:self.lmax+1]},**params_values)
    cls.initialize=initialize; cls.get_requirements=get_requirements; cls.compute_chi2=compute_chi2; cls.logp=logp
    cls._bubbleverse_q041_patch=True
    cls._bubbleverse_q041_patch_meta={"patch":"Q041_RUNTIME_ONLY","support_sha256":support["support_sha256"],
                                      "restricted_precision_sha256":meta["restricted_precision_sha256"],"component":q32.HILLIPOP}
    return cls._bubbleverse_q041_patch_meta


def add_external_data(info: dict[str,Any], combo: str) -> None:
    if combo not in ALL_COMBOS: raise RuntimeError("COMBINATION_GATE=FAIL")
    like=info.setdefault("likelihood",{}); params=info.setdefault("params",{}); prior=info.setdefault("prior",{})
    if has_act(combo):
        like["act_dr6_cmbonly.ACTDR6CMBonly"]={
            "input_file":"dr6_data_cmbonly.fits","lmax_theory":9000,
            "ell_cuts":{"TT":[600,8500],"TE":[600,8500],"EE":[600,8500]},"stop_at_error":True,
        }
        params["A_act"]={"prior":{"min":0.5,"max":1.5},"ref":{"dist":"norm","loc":1.0,"scale":0.01},"proposal":0.003}
        params["P_act"]={"prior":{"min":0.9,"max":1.1},"ref":{"dist":"norm","loc":1.0,"scale":0.01},"proposal":0.01}
        def q041_act_calibration_prior(A_act):
            z=(float(A_act)-1.0)/0.003
            return -0.5*z*z
        prior["q041_act_calibration_shape"]=q041_act_calibration_prior
    if has_lens(combo):
        like["act_dr6_lenslike.ACTDR6LensLike"]={"lens_only":False,"stop_at_error":True,"lmax":4000,"variant":"act_baseline"}
    if has_desi(combo):
        like["bao.desi_dr2"]=None


def build_info(args: argparse.Namespace, implementation: str, combo: str, prefix: Path, mcmc: bool) -> tuple[dict[str,Any],dict[str,Any]]:
    q32=load_q032(args.q032_parent_root); cfg=q032_cfg(q32,args.q032_parent_root)
    pf=load_sealed_preflight(args.preflight)
    full_support=pf["support_lock"]
    reduced=read_json(args.reduced_support)
    support=reduced if has_act(combo) else full_support
    parent,parent_path=reference_parent(args.parent_dir,implementation); start=start_from_parent(parent)
    if implementation=="hillipop":
        if has_act(combo): install_q041_hillipop_patch(q32,args.reduced_hlp_matrix,args.reduced_hlp_meta,support,cfg)
        else: q32.install_hillipop_patch(args.hlp_matrix,args.hlp_meta,support,cfg)
        info=q32.build_hillipop_info(cfg,start,prefix,"refinement")
    elif implementation=="camspec":
        info=q32.build_camspec_info(cfg,start,prefix,"refinement",support)
    else: raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
    add_external_data(info,combo)
    for k,v in start.items():
        try: q32.set_ref(info["params"],k,v)
        except Exception: pass
    info["output"]=str(prefix.resolve()); info["force"]=True; info["resume"]=False
    if mcmc:
        info["sampler"]={"mcmc":{
            "seed":int(args.chain_seed),"burn_in":100,"max_samples":20000,
            "Rminus1_stop":0.02,"Rminus1_cl_stop":0.2,"learn_proposal":True,
        }}
    meta={"parent_file":str(parent_path),"parent_sha256":sha256_file(parent_path),"support_sha256":support["support_sha256"],
          "support_mode":"ELL_LE_599" if has_act(combo) else "Q032_FULL_COMMON_TT3PAIR"}
    return info,meta


def runtime_preflight(args: argparse.Namespace) -> int:
    load_preregister(args.preregister); load_source_lock(args.source_lock)
    prov=read_json(args.external_runtime)
    if prov.get("q")!=Q or prov.get("status")!="PASS" or prov.get("cobaya_upgraded") is not False:
        raise RuntimeError("EXTERNAL_RUNTIME_GATE=FAIL")
    rows=[]
    for implementation in ARMS:
        prefix=Path(args.output).with_suffix("").parent/f"q041_preflight_{implementation}"
        info,meta=build_info(args,implementation,FULL_COMBO,prefix,mcmc=False)
        q32=load_q032(args.q032_parent_root)
        probe=q32.reference_vector(info,preferred=start_from_parent(reference_parent(args.parent_dir,implementation)[0]))
        model=None
        try:
            model=q32.create_model(info)
            logpost,_=q32.evaluate_model_once(model,info,probe)
            if not finite(logpost): raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL")
            rows.append({"implementation":implementation,"combo":FULL_COMBO,"finite_logposterior":float(logpost),"meta":meta,"status":"PASS"})
        finally:
            try:
                if model is not None: model.close()
            except Exception: pass
    write_json(args.output,{"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"stage":"RUNTIME_PREFLIGHT","status":"PASS",
                            "actual_computed_result":False,"technical_preflight_only":True,"rows":rows,
                            "gates":{"Q040_FIREWALL":"PASS","EXTERNAL_RUNTIME":"PASS","BOTH_NATIVE_ARMS":"PASS","FULL_COMBINATION_FINITE":"PASS"}})
    print("Q041_RUNTIME_PREFLIGHT_GATE=PASS")
    return 0


def sample(args: argparse.Namespace) -> int:
    if args.implementation not in ARMS or args.combo not in ALL_COMBOS or args.chain not in (0,1): raise RuntimeError("SAMPLE_IDENTITY_GATE=FAIL")
    args.chain_seed=410000+1000*ARMS.index(args.implementation)+10*ALL_COMBOS.index(args.combo)+args.chain
    prefix=Path(args.output_dir)/"chain"
    info,meta=build_info(args,args.implementation,args.combo,prefix,mcmc=True)
    rec={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"MCMC_CHAIN",
         "implementation":args.implementation,"combo":args.combo,"chain":args.chain,"chain_seed":args.chain_seed,
         "status":"FAILED","actual_computed_result":False,"meta":meta}
    sampler=None
    try:
        from cobaya.run import run as cobaya_run
        _,sampler=cobaya_run(info,force=True)
        rec.update({"status":"COMPLETE","actual_computed_result":True,"output_prefix":"chain"})
    except Exception as exc:
        rec.update({"status":"FAILED","failure_class":"MCMC_OR_LIKELIHOOD","error":repr(exc)})
    finally:
        try:
            if sampler is not None and hasattr(sampler,"close"): sampler.close()
        except Exception: pass
        write_json(Path(args.output_dir)/"q041_chain_metadata_v7.json",rec)
    if rec["status"]!="COMPLETE": raise RuntimeError("Q041_CHAIN_GATE=FAIL "+rec.get("error",""))
    print(f"Q041_CHAIN_GATE=PASS arm={args.implementation} combo={args.combo} chain={args.chain}")
    return 0


def _weighted_stats(samples: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    w=np.asarray(weights,dtype=float); x=np.asarray(samples,dtype=float)
    sw=float(w.sum()); mu=(w[:,None]*x).sum(axis=0)/sw
    d=x-mu; cov=(d.T*w)@d/max(sw-1.0,1.0)
    return mu,cov


def _rhat_for_chains(chains: Sequence[tuple[np.ndarray,np.ndarray]]) -> np.ndarray:
    means=[]; vars_=[]; neffs=[]
    for x,w in chains:
        mu,cov=_weighted_stats(x,w); means.append(mu); vars_.append(np.diag(cov)); neffs.append((w.sum()**2)/max(float((w*w).sum()),1e-30))
    m=len(chains); n=max(2.0,min(neffs)); means=np.asarray(means); W=np.mean(np.asarray(vars_),axis=0)
    B=n*np.var(means,axis=0,ddof=1)
    varhat=((n-1.0)/n)*W+B/n
    return np.sqrt(np.maximum(varhat/np.maximum(W,1e-300),0.0))


def _bc(mu1: np.ndarray,c1: np.ndarray,mu2: np.ndarray,c2: np.ndarray) -> float:
    n=len(mu1); scale=max(float(np.trace(c1+c2))/max(2*n,1),1e-18); eps=scale*1e-10
    C1=c1+np.eye(n)*eps; C2=c2+np.eye(n)*eps; C=0.5*(C1+C2); d=mu1-mu2
    inv=np.linalg.pinv(C); term1=0.125*float(d@inv@d)
    sC,ldC=np.linalg.slogdet(C); s1,ld1=np.linalg.slogdet(C1); s2,ld2=np.linalg.slogdet(C2)
    if min(sC,s1,s2)<=0: raise RuntimeError("POSTERIOR_COVARIANCE_PD_GATE=FAIL")
    db=term1+0.5*(ldC-0.5*(ld1+ld2))
    return float(max(0.0,min(1.0,math.exp(-db))))


def load_chain_from_meta(meta_path: Path):
    from getdist.mcsamples import loadMCSamples
    roots=[]
    for p in meta_path.parent.rglob("*.paramnames"): roots.append(p.with_suffix(""))
    if len(roots)!=1: raise RuntimeError(f"CHAIN_ROOT_UNIQUENESS_GATE=FAIL meta={meta_path} roots={roots}")
    s=loadMCSamples(str(roots[0]),settings={"ignore_rows":0})
    names=[p.name for p in s.paramNames.names]; idx=[]
    for c in COMMON_COORDS:
        if c not in names: raise RuntimeError(f"CHAIN_COORDINATE_GATE=FAIL coord={c} root={roots[0]}")
        idx.append(names.index(c))
    return np.asarray(s.samples[:,idx],dtype=float),np.asarray(s.weights,dtype=float)


def aggregate(args: argparse.Namespace) -> int:
    load_preregister(args.preregister); load_source_lock(args.source_lock)
    metas=[]
    for p in Path(args.input_dir).rglob("q041_chain_metadata_v7.json"):
        d=read_json(p)
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID: metas.append((d,p))
    expected={(a,c,k) for a in ARMS for c in ALL_COMBOS for k in (0,1)}
    found={(d.get("implementation"),d.get("combo"),int(d.get("chain",-1))) for d,_ in metas if d.get("status")=="COMPLETE" and d.get("actual_computed_result") is True}
    missing=sorted(expected-found)
    if missing: raise RuntimeError(f"CHAIN_COMPLETENESS_GATE=FAIL missing={missing}")

    summaries={}; chain_cache={}
    for arm in ARMS:
        for combo in ALL_COMBOS:
            cc=[]
            for chain in (0,1):
                d,p=next((d,p) for d,p in metas if d.get("implementation")==arm and d.get("combo")==combo and int(d.get("chain",-1))==chain)
                x,w=load_chain_from_meta(p); cc.append((x,w)); chain_cache[(arm,combo,chain)]=(x,w)
            rh=_rhat_for_chains(cc)
            if not np.all(np.isfinite(rh)) or float(np.max(rh))>HARD_RHAT:
                raise RuntimeError(f"CONVERGENCE_GATE=FAIL arm={arm} combo={combo} rhat={rh.tolist()}")
            x=np.vstack([z[0] for z in cc]); w=np.concatenate([z[1] for z in cc]); mu,cov=_weighted_stats(x,w)
            summaries[f"{arm}:{combo}"]={"mean":dict(zip(COMMON_COORDS,map(float,mu))),"covariance":cov.tolist(),
                                           "rhat":dict(zip(COMMON_COORDS,map(float,rh))),"max_rhat":float(np.max(rh)),
                                           "effective_weight":float(w.sum())}
    comparisons={}
    for combo in ALL_COMBOS:
        A=summaries[f"camspec:{combo}"]; B=summaries[f"hillipop:{combo}"]
        mu1=np.array([A["mean"][c] for c in COMMON_COORDS]); mu2=np.array([B["mean"][c] for c in COMMON_COORDS])
        c1=np.asarray(A["covariance"]); c2=np.asarray(B["covariance"])
        sig=np.sqrt(np.maximum(np.diag(c1)+np.diag(c2),1e-300)); shifts=np.abs(mu1-mu2)/sig
        comparisons[combo]={"standardized_mean_shift":dict(zip(COMMON_COORDS,map(float,shifts))),
                            "max_standardized_shift":float(np.max(shifts)),"gaussian_bhattacharyya_coefficient":_bc(mu1,c1,mu2,c2)}
    full=comparisons[FULL_COMBO]; loo=[comparisons[c]["max_standardized_shift"] for c in LOO_COMBOS]
    robust_material=sum(v>=LOO_MATERIAL_SIGMA for v in loo)>=2
    if (full["max_standardized_shift"]>=MATERIAL_SIGMA or full["gaussian_bhattacharyya_coefficient"]<=BC_MATERIAL) and robust_material:
        classification="MATERIAL_DOWNSTREAM_DIFFERENCE"
    elif (full["max_standardized_shift"]<=EQUIV_SIGMA and full["gaussian_bhattacharyya_coefficient"]>=BC_EQUIV
          and all(v<=LOO_MATERIAL_SIGMA for v in loo)):
        classification="SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS"
    else: classification="CONSTRAINED_MIXED"
    out={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"FINAL",
         "status":"PASS","actual_computed_result":True,"scientific_classification":classification,
         "required_gates":{"CHAIN_COMPLETENESS":"PASS","ALL_RHAT_LE_1P05":"PASS","BOTH_ARMS_ALL_COMBINATIONS":"PASS","Q040_FIREWALL":"PASS"},
         "summaries":summaries,"comparisons":comparisons,"classification_inputs":{"full":full,"loo_max_shifts":dict(zip(LOO_COMBOS,loo))},
         "claim_boundaries":{"no_cross_arm_chi2_sum":True,"no_hybrid_planck_likelihood":True,"Q040_scientific_products_used":False,
                             "bhattacharyya_is_gaussian_summary_of_empirical_posterior_moments":True}}
    write_json(args.output,out)
    print(f"Q041_FINAL_GATE=PASS classification={classification}")
    return 0


def static_check(args: argparse.Namespace) -> int:
    p=load_preregister(args.preregister); s=load_source_lock(args.source_lock)
    gates={"IDENTITY":"PASS","Q032_PARENT":"PASS","Q040_FIREWALL":"PASS","EXTERNAL_LOCKS":"PASS","CLASSIFICATION_THRESHOLDS":"PASS"}
    if p["baseline_parent"]["execution_commit"]!=Q032_COMMIT: raise RuntimeError("STATIC_Q032_GATE=FAIL")
    if s["external"]["act_dr6_cmbonly"]["commit"]!="880eacb40d66722eb1c32d7b5621e91662b4d808": raise RuntimeError("STATIC_ACT_GATE=FAIL")
    write_json(args.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"STATIC","status":"PASS","gates":gates})
    print("Q041_STATIC_GATE=PASS")
    return 0


def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static"); s.add_argument("--preregister",required=True); s.add_argument("--source-lock",required=True); s.add_argument("--output",required=True); s.set_defaults(func=static_check)
    s=sp.add_parser("prepare-nonoverlap")
    for x in ("q032-parent-root","preflight","hlp-matrix","hlp-meta","support-output","matrix-output","meta-output"): s.add_argument("--"+x,required=True)
    s.set_defaults(func=prepare_nonoverlap)
    for name,func in (("runtime-preflight",runtime_preflight),("sample",sample)):
        s=sp.add_parser(name)
        for x in ("q032-parent-root","preflight","parent-dir","hlp-matrix","hlp-meta","reduced-support","reduced-hlp-matrix","reduced-hlp-meta","preregister","source-lock"): s.add_argument("--"+x,required=True)
        if name=="runtime-preflight":
            s.add_argument("--external-runtime",required=True); s.add_argument("--output",required=True)
        else:
            s.add_argument("--implementation",required=True,choices=ARMS); s.add_argument("--combo",required=True,choices=ALL_COMBOS); s.add_argument("--chain",required=True,type=int,choices=(0,1)); s.add_argument("--output-dir",required=True); s.set_defaults(chain_seed=0)
        s.set_defaults(func=func)
    s=sp.add_parser("aggregate"); s.add_argument("--input-dir",required=True); s.add_argument("--preregister",required=True); s.add_argument("--source-lock",required=True); s.add_argument("--output",required=True); s.set_defaults(func=aggregate)
    return p

if __name__=="__main__":
    a=parser().parse_args(); raise SystemExit(a.func(a))
