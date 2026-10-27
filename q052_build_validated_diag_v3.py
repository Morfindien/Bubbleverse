#!/usr/bin/env python3
"""Build Q052-VALIDATEDDIAG-V3 from the immutable Q052-NATIVEPAIR-V2 C wrapper.

This is a fail-closed source-to-source instrumentation step. It does not alter
hydrogen/helium equations, selector rules, z=810 intervention semantics, fixed
z_reio, solver choice, tolerances, or the historical V2 file. It only emits a
new C translation unit with diagnostic exports.
"""
from __future__ import annotations
import argparse, hashlib, subprocess
from pathlib import Path

EXPECTED_BASE_GIT_BLOB = "0539a22cb503af2030c4ca6cdbc7f0c41ba6e1f7"
EXPECTED_BASE_SHA256 = "d67bf8f8116c835864150d50fda258a0ec33258bfef258accd374dd395acbb4a"
NEW_ID = "Q052-VALIDATEDDIAG-V3"

DIAG_BLOCK = r'''
/* Q052-VALIDATEDDIAG-V3: diagnostic-only capture. No physics formula is changed. */
static unsigned long q052_diag_rhs_count=0, q052_diag_output_count=0, q052_diag_guard_count=0;
static __thread int q052_guard_active=0, q052_guard_hmla=0, q052_guard_tla=0, q052_guard_swift=0;

static FILE *q052_diag_append(const char *name){return open_out(name,"a");}
static void q052_diag_arr(FILE *f,const double *x,int n){
  fputc('[',f); for(int i=0;i<n;i++){if(i)fputc(',',f);jhex(f,x[i]);} fputc(']',f);
}
static void q052_diag_state(const char *tag,double mz,double *y,double *dy,
                            struct thermodynamics_parameters_and_workspace *a,int index_z){
  if(!intervention_active)return;
  struct thermo_diffeq_workspace *d=a->ptw->ptdw; struct thermo_vector *v=d->ptv;
  if(!v||!y||!dy||v->ti_size<=0)die("DIAG_VECTOR");
  FILE *f=q052_diag_append("fullstate_trace.jsonl");
  fputs("{\"schema\":\"Q052_FULLSTATE_TRACE_V3\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);
  fputs(",\"arm\":",f);js(f,arm);fputs(",\"mode\":",f);js(f,mode);fputs(",\"tag\":",f);js(f,tag);
  fprintf(f,",\"index_z\":%d,\"phase\":%d,\"require_H\":%d,\"require_He\":%d,\"ti_size\":%d",
          index_z,d->ap_current,d->require_H,d->require_He,v->ti_size);
  fputs(",\"mz\":",f);jhex(f,mz);fputs(",\"z\":",f);jhex(f,-mz);
  fprintf(f,",\"indices\":{\"D_Tmat\":%d,\"x_H\":%d,\"x_He\":%d,\"T_idm\":%d}",
          v->index_ti_D_Tmat,v->index_ti_x_H,v->index_ti_x_He,v->index_ti_T_idm);
  fputs(",\"y\":",f);q052_diag_arr(f,y,v->ti_size);fputs(",\"dy\":",f);q052_diag_arr(f,dy,v->ti_size);
  fputs(",\"workspace\":{\"x_H\":",f);jhex(f,d->x_H);fputs(",\"x_He\":",f);jhex(f,d->x_He);
  fputs(",\"x_noreio\":",f);jhex(f,d->x_noreio);fputs(",\"x_reio\":",f);jhex(f,d->x_reio);
  fputs(",\"Tmat_K\":",f);jhex(f,d->Tmat);fputs("}",f);
  double tg=a->ptw->Tcmb*(1.0-mz); double D=y[v->index_ti_D_Tmat];
  fputs(",\"Tgamma_K\":",f);jhex(f,tg);fputs(",\"Tmat_over_Trad\":",f);jhex(f,(D+tg)/tg);
  fprintf(f,",\"background_snapshot_kind\":\"workspace_after_original_callback\",\"background_size_normal\":%d,\"pvecback_normal\":",a->pba->bg_size_normal);
  q052_diag_arr(f,a->pvecback,a->pba->bg_size_normal);fputs("}\n",f);close_ok(f);
  if(index_z>=0)q052_diag_output_count++;else q052_diag_rhs_count++;
}
static void q052_diag_boundary(const char *tag,double mz,struct thermodynamics_parameters_and_workspace *a){
  struct thermo_diffeq_workspace *d=a->ptw->ptdw; struct thermo_vector *v=d->ptv;
  if(!v||!v->y)die("DIAG_BOUNDARY_VECTOR");
  FILE *f=q052_diag_append("event_phase_trace.jsonl");
  fputs("{\"schema\":\"Q052_EVENT_PHASE_TRACE_V3\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);
  fputs(",\"arm\":",f);js(f,arm);fputs(",\"tag\":",f);js(f,tag);fputs(",\"mz\":",f);jhex(f,mz);fputs(",\"z\":",f);jhex(f,-mz);
  fprintf(f,",\"phase\":%d,\"require_H\":%d,\"require_He\":%d,\"ti_size\":%d,\"y\":",d->ap_current,d->require_H,d->require_He,v->ti_size);
  q052_diag_arr(f,v->y,v->ti_size);fputs(",\"ap_z_limits\":",f);q052_diag_arr(f,d->ap_z_limits,d->ap_size);
  fputs(",\"ap_z_limits_delta\":",f);q052_diag_arr(f,d->ap_z_limits_delta,d->ap_size);
  fprintf(f,",\"background_size_normal\":%d,\"pvecback_normal\":",a->pba->bg_size_normal);q052_diag_arr(f,a->pvecback,a->pba->bg_size_normal);
  fputs(",\"derivative_at_boundary_certified\":false}\n",f);close_ok(f);
}

typedef double (*q052_rec_dx_fn)(HYREC_DATA*,int,double,double,double,double,double,double,unsigned,double);
typedef double (*q052_hmla_fn)(HYREC_DATA*,double,double,double,double,double,double);
typedef double (*q052_tla_fn)(REC_COSMOPARAMS*,double,double,double,double,double,double,double);
typedef double (*q052_swift_fn)(HYREC_DATA*,double,double,double,double,double,double,double);

double rec_HMLA_dxHIIdlna(HYREC_DATA *d,double xe,double xHII,double nH,double H,double TM,double TR){
  static q052_hmla_fn fn=NULL;if(!fn)fn=(q052_hmla_fn)original("rec_HMLA_dxHIIdlna");if(q052_guard_active)q052_guard_hmla++;return fn(d,xe,xHII,nH,H,TM,TR);
}
double rec_TLA_dxHIIdlna(REC_COSMOPARAMS *c,double xe,double xHII,double nH,double H,double TM,double TR,double fudge){
  static q052_tla_fn fn=NULL;if(!fn)fn=(q052_tla_fn)original("rec_TLA_dxHIIdlna");if(q052_guard_active)q052_guard_tla++;return fn(c,xe,xHII,nH,H,TM,TR,fudge);
}
double rec_swift_hyrec_dxHIIdlna(HYREC_DATA *d,double xe,double xHII,double nH,double H,double TM,double TR,double z){
  static q052_swift_fn fn=NULL;if(!fn)fn=(q052_swift_fn)original("rec_swift_hyrec_dxHIIdlna");if(q052_guard_active)q052_guard_swift++;return fn(d,xe,xHII,nH,H,TM,TR,z);
}
double rec_dxHIIdlna(HYREC_DATA *d,int model,double xe,double xHII,double nH,double H,double TM,double TR,unsigned iz,double z){
  static q052_rec_dx_fn fn=NULL;if(!fn)fn=(q052_rec_dx_fn)original("rec_dxHIIdlna");
  q052_guard_hmla=q052_guard_tla=q052_guard_swift=0;q052_guard_active=intervention_active;
  double r=fn(d,model,xe,xHII,nH,H,TM,TR,iz,z);int active=q052_guard_active;q052_guard_active=0;
  if(active){FILE *f=q052_diag_append("hyrec_guard_trace.jsonl");
    fputs("{\"schema\":\"Q052_HYREC_GUARD_TRACE_V3\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);fputs(",\"arm\":",f);js(f,arm);
    fprintf(f,",\"model_observed\":%d,\"iz\":%u,\"z\":",model,iz);jhex(f,z);fputs(",\"xe\":",f);jhex(f,xe);fputs(",\"xHII\":",f);jhex(f,xHII);
    fputs(",\"nH_cm3\":",f);jhex(f,nH);fputs(",\"H_per_s\":",f);jhex(f,H);fputs(",\"TM_eV\":",f);jhex(f,TM);fputs(",\"TR_eV\":",f);jhex(f,TR);
    fprintf(f,",\"observed_child_calls\":{\"HMLA\":%d,\"TLA\":%d,\"SWIFT\":%d},\"result\":",q052_guard_hmla,q052_guard_tla,q052_guard_swift);jhex(f,r);
    fputs(",\"Pion_value_captured\":false,\"guard_values_must_be_reconstructed_from_pinned_source\":true}\n",f);close_ok(f);q052_diag_guard_count++;}
  return r;
}
static void q052_diag_finalize(struct background *ba){
  FILE *f=open_out("diagnostic_manifest.json","wx");
  fputs("{\"schema\":\"Q052_DIAGNOSTIC_MANIFEST_V3\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);fputs(",\"arm\":",f);js(f,arm);
  fprintf(f,",\"rhs_records\":%lu,\"output_records\":%lu,\"guard_records\":%lu,\"background_indices\":{\"a\":%d,\"H\":%d,\"H_prime\":%d,\"rho_b\":%d,\"rho_g\":%d,\"rho_ur\":%d,\"rho_scf\":%d,\"p_scf\":%d,\"V_scf\":%d,\"V_e_scf\":%d},\"capture_scope\":\"diagnostic_only_not_validated_interval_certificate\"}\n",
          q052_diag_rhs_count,q052_diag_output_count,q052_diag_guard_count,ba->index_bg_a,ba->index_bg_H,ba->index_bg_H_prime,ba->index_bg_rho_b,ba->index_bg_rho_g,ba->index_bg_rho_ur,ba->index_bg_rho_scf,ba->index_bg_p_scf,ba->index_bg_V_scf,ba->index_bg_V_e_scf);
  close_ok(f);
}
'''


def one(text: str, old: str, new: str, label: str) -> str:
    n=text.count(old)
    if n != 1:
        raise RuntimeError(f"PATCH_ANCHOR_{label}_COUNT={n}")
    return text.replace(old,new,1)


def patch_source(text: str) -> str:
    text=one(text,'#define Q052_ID "Q052-NATIVEPAIR-V2"','#define Q052_ID "Q052-VALIDATEDDIAG-V3"','ID')
    anchor='static void jhex(FILE *f,double x){if(!isfinite(x))die("NONFINITE");fprintf(f,"\\\"%a\\\"",x);}\nstatic double tol_scale(void)'
    text=one(text,anchor,anchor.split('\nstatic double tol_scale(void)')[0]+'\n'+DIAG_BLOCK+'\nstatic double tol_scale(void)','DIAG_BLOCK')
    old='''  if(rc==_SUCCESS_ && intervention_active){\n    struct thermo_vector *v=a->ptw->ptdw->ptv;\n    dy[v->index_ti_x_He]=0.;\n    y[v->index_ti_x_He]=q_xHeII/a->ptw->fHe;\n    for(int i=0;i<v->ti_size;i++) if(!isfinite(dy[i])){snprintf(err,_ERRORMSGSIZE_,"Q052_NONFINITE_DERIV");return _FAILURE_;}\n  }\n  return rc;\n}'''
    new=old.replace('  return rc;','  if(rc==_SUCCESS_ && intervention_active)q052_diag_state("RHS",x,y,dy,a,-1);\n  return rc;')
    text=one(text,old,new,'RHS')
    old='''  int rc=original_sources(x,y,dy,index_z,workspace,err);\n  if(rc==_SUCCESS_ && intervention_active) enforce_q(a,y);\n  return rc;\n}'''
    new='''  int rc=original_sources(x,y,dy,index_z,workspace,err);\n  if(rc==_SUCCESS_ && intervention_active){enforce_q(a,y);q052_diag_state("OUTPUT",x,y,dy,a,index_z);}\n  return rc;\n}'''
    text=one(text,old,new,'OUTPUT')
    old='''    class_call(background_at_z(pba,-limits[interval],normal_info,inter_normal,\n                               &(ptw->last_index_back),pvecback),\n               pba->error_message,pth->error_message);'''
    new=old+'\n    q052_diag_boundary("PHASE_ENTRY",limits[interval],&tpaw);'
    text=one(text,old,new,'PHASE_ENTRY')
    old='''      write_start(&tpaw,Q052_MZ_EVENT);\n      intervention_active=1;\n      enforce_q(&tpaw,ptw->ptdw->ptv->y);'''
    new='''      write_start(&tpaw,Q052_MZ_EVENT);\n      q052_diag_boundary("Z810_PRE_INTERVENTION",Q052_MZ_EVENT,&tpaw);\n      intervention_active=1;\n      enforce_q(&tpaw,ptw->ptdw->ptv->y);\n      q052_diag_boundary("Z810_POST_INTERVENTION",Q052_MZ_EVENT,&tpaw);'''
    text=one(text,old,new,'EVENT')
    old='''  effective(&ba,&th);\n  history(&th);\n  FILE *f=open_out("runtime_result.json","wx");'''
    new='''  effective(&ba,&th);\n  history(&th);\n  q052_diag_finalize(&ba);\n  FILE *f=open_out("runtime_result.json","wx");'''
    text=one(text,old,new,'FINALIZE')
    required=[NEW_ID,'fullstate_trace.jsonl','hyrec_guard_trace.jsonl','event_phase_trace.jsonl','diagnostic_manifest.json','Pion_value_captured']
    for token in required:
        if token not in text: raise RuntimeError('PATCH_OUTPUT_MISSING '+token)
    return text


def git_blob(path: Path) -> str|None:
    try:
        return subprocess.check_output(['git','hash-object',str(path)],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def gate_base(path: Path) -> str:
    raw=path.read_bytes(); h=hashlib.sha256(raw).hexdigest(); b=git_blob(path)
    if h != EXPECTED_BASE_SHA256:
        raise RuntimeError(f"BASE_SHA256_MISMATCH expected={EXPECTED_BASE_SHA256} actual={h}")
    if b is not None and b != EXPECTED_BASE_GIT_BLOB:
        raise RuntimeError(f"BASE_GIT_BLOB_MISMATCH expected={EXPECTED_BASE_GIT_BLOB} actual={b}")
    return raw.decode()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',default='q052_native_pair_v2.c');ap.add_argument('--output',default='q052_validated_diag_v3.c');ap.add_argument('--check-only',action='store_true');a=ap.parse_args()
    src=gate_base(Path(a.base)); out=patch_source(src)
    if a.check_only:
        print('Q052_VALIDATEDDIAG_V3_PATCH_GATE=PASS');return
    p=Path(a.output);p.write_text(out);print(f'Q052_VALIDATEDDIAG_V3_GENERATED={p}')

if __name__=='__main__':main()
