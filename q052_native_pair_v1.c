/* Bubbleverse Q052-NATIVEPAIR-V1
 *
 * Native intervention wrapper for the pinned mwt5345/class_ede source lineage.
 * It does NOT reimplement hydrogen physics. It interposes only orchestration:
 *   1) original CLASS thermodynamics up to an exact z=810 NDF15 boundary,
 *   2) one controlled helium endpoint intervention q=xHeII,
 *   3) original thermodynamics_derivs / thermodynamics_sources afterwards,
 *      with helium held constant and every other active equation source-real.
 *
 * The executable must be linked against the already hash-pinned original classy.so.
 */
#define _GNU_SOURCE
#include "class.h"
#include "wrap_hyrec.h"
#include <dlfcn.h>
#include <fenv.h>
#include <float.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define Q052_ID "Q052-NATIVEPAIR-V1"
#define Q052_Z_EVENT 810.0
#define Q052_MZ_EVENT -810.0

typedef int (*derivs_fn)(double,double*,double*,void*,ErrorMsg);
typedef int (*sources_fn)(double,double*,double*,int,void*,ErrorMsg);

static derivs_fn original_derivs = NULL;
static sources_fn original_sources = NULL;
static const char *outdir = NULL;
static const char *arm = NULL;
static const char *mode = NULL;
static const char *run_id = NULL;
static double q_xHeII = 0.0;
static int intervention_active = 0;
static int solve_interposed = 0;
static int start_written = 0;

static void die(const char *msg){fprintf(stderr,"Q052_NATIVEPAIR_FAIL %s\n",msg);exit(90);}
static void *original(const char *name){
  dlerror(); void *p=dlsym(RTLD_NEXT,name);
  if(!p){fprintf(stderr,"Q052_DLSYM_FAIL %s %s\n",name,dlerror());exit(91);}
  return p;
}
static FILE *open_out(const char *name,const char *mode_s){
  char p[4096];
  if(!outdir || snprintf(p,sizeof p,"%s/%s",outdir,name)>=(int)sizeof p) die("OUTPUT_PATH");
  FILE *f=fopen(p,mode_s); if(!f) die("OUTPUT_OPEN"); return f;
}
static void close_ok(FILE *f){if(ferror(f)||fclose(f))die("OUTPUT_WRITE");}
static void js(FILE *f,const char *s){
  fputc('"',f); for(;*s;s++){unsigned char c=(unsigned char)*s;
    if(c=='"'||c=='\\'){fputc('\\',f);fputc(c,f);}
    else if(c<32)fprintf(f,"\\u%04x",c); else fputc(c,f);} fputc('"',f);
}
static void jhex(FILE *f,double x){if(!isfinite(x))die("NONFINITE");fprintf(f,"\"%a\"",x);}
static double tol_scale(void){return strcmp(mode,"refined")==0 ? 0.1 : 1.0;}
static double step_scale(void){return strcmp(mode,"refined")==0 ? 0.5 : 1.0;}

static void enforce_q(struct thermodynamics_parameters_and_workspace *a,double *y){
  struct thermo_diffeq_workspace *d=a->ptw->ptdw;
  struct thermo_vector *v=d->ptv;
  if(!v || v->ti_size<3 || v->index_ti_x_He<0 || !(a->ptw->fHe>0.)) die("HELIUM_VECTOR");
  y[v->index_ti_x_He]=q_xHeII/a->ptw->fHe;
  d->require_He=_FALSE_;
}

int thermodynamics_derivs(double x,double *y,double *dy,void *workspace,ErrorMsg err){
  if(!original_derivs) original_derivs=(derivs_fn)original("thermodynamics_derivs");
  struct thermodynamics_parameters_and_workspace *a=workspace;
  if(intervention_active){
    struct thermo_diffeq_workspace *d=a->ptw->ptdw;
    struct thermo_vector *v=d->ptv;
    enforce_q(a,y);
    for(int i=0;i<v->ti_size;i++)dy[i]=0.;
  }
  int rc=original_derivs(x,y,dy,workspace,err);
  if(rc==_SUCCESS_ && intervention_active){
    struct thermo_vector *v=a->ptw->ptdw->ptv;
    dy[v->index_ti_x_He]=0.;
    y[v->index_ti_x_He]=q_xHeII/a->ptw->fHe;
    for(int i=0;i<v->ti_size;i++) if(!isfinite(dy[i])){snprintf(err,_ERRORMSGSIZE_,"Q052_NONFINITE_DERIV");return _FAILURE_;}
  }
  return rc;
}

int thermodynamics_sources(double x,double *y,double *dy,int index_z,void *workspace,ErrorMsg err){
  if(!original_sources) original_sources=(sources_fn)original("thermodynamics_sources");
  struct thermodynamics_parameters_and_workspace *a=workspace;
  if(intervention_active) enforce_q(a,y);
  int rc=original_sources(x,y,dy,index_z,workspace,err);
  if(rc==_SUCCESS_ && intervention_active) enforce_q(a,y);
  return rc;
}

static void write_start(struct thermodynamics_parameters_and_workspace *a,double mz){
  if(start_written) die("START_DUPLICATE");
  struct thermo_diffeq_workspace *d=a->ptw->ptdw;
  struct thermo_vector *v=d->ptv;
  if(d->ap_current!=d->index_ap_frec || !v || !d->require_H || !d->require_He) die("START_PHASE");
  double Trad=a->ptw->Tcmb*(1.0-mz);
  double D=v->y[v->index_ti_D_Tmat];
  double h=v->y[v->index_ti_x_H];
  double he=v->y[v->index_ti_x_He];
  double vratio=(D+Trad)/Trad;
  FILE *f=open_out("z810_start.json","wx");
  fputs("{\"schema\":\"Q052_Z810_START_V1\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);
  fputs(",\"arm\":",f);js(f,arm);fputs(",\"mode\":",f);js(f,mode);
  fputs(",\"mz\":",f);jhex(f,mz);fputs(",\"z\":",f);jhex(f,-mz);
  fputs(",\"D_Tmat_K\":",f);jhex(f,D);fputs(",\"x_H\":",f);jhex(f,h);fputs(",\"x_He_pre\":",f);jhex(f,he);
  fputs(",\"fHe_CLASS\":",f);jhex(f,a->ptw->fHe);fputs(",\"xHeII_pre\":",f);jhex(f,a->ptw->fHe*he);
  fputs(",\"Tgamma_K\":",f);jhex(f,Trad);fputs(",\"Tmat_over_Trad\":",f);jhex(f,vratio);
  fputs(",\"q_xHeII_post\":",f);jhex(f,q_xHeII);
  fputs(",\"native_xHeII_limit\":",f);jhex(f,d->phyrec->xHeII_limit);
  fprintf(f,",\"phase\":%d,\"index_ap_frec\":%d,\"require_H\":%d,\"require_He_pre\":%d}\n",
          d->ap_current,d->index_ap_frec,d->require_H,d->require_He);
  close_ok(f); start_written=1;
}

static int evolve(int (*ev)(),double a,double b,double *mz_output,int mz_size,
                  struct thermodynamics_parameters_and_workspace *tpaw){
  struct precision *ppr=tpaw->ppr; struct thermo_vector *v=tpaw->ptw->ptdw->ptv;
  return ev(thermodynamics_derivs,a,b,v->y,v->used_in_output,v->ti_size,tpaw,
            ppr->tol_thermo_integration*tol_scale(),
            ppr->smallest_allowed_variation,
            thermodynamics_timescale,
            ppr->thermo_integration_stepsize*step_scale(),
            mz_output,mz_size,thermodynamics_sources,NULL,tpaw->pth->error_message);
}

/* Deliberately mirrors the pinned source orchestration, adding exactly one new
 * event boundary at z=810 inside frec. No selector/rate formula is copied here.
 */
int thermodynamics_solve(struct precision *ppr,struct background *pba,
                         struct thermodynamics *pth,struct thermo_workspace *ptw,
                         double *pvecback){
  extern int evolver_rk();
  extern int evolver_ndf15();
  int (*generic_evolver)()=evolver_ndf15;
  if(ppr->thermo_evolver==rk) generic_evolver=evolver_rk;
  else if(ppr->thermo_evolver!=ndf15){snprintf(pth->error_message,_ERRORMSGSIZE_,"Q052_EVOLVER");return _FAILURE_;}
  if(pth->reio_z_or_tau!=reio_z){snprintf(pth->error_message,_ERRORMSGSIZE_,"Q052_TAU_SHOOTING_FORBIDDEN");return _FAILURE_;}

  struct thermodynamics_parameters_and_workspace tpaw={pba,ppr,pth,ptw,pvecback};
  double *mz_output=NULL,*limits=NULL;
  class_alloc(mz_output,pth->tt_size*sizeof(double),pth->error_message);
  for(int i=0;i<pth->tt_size;i++)mz_output[i]=-pth->z_table[pth->tt_size-1-i];
  class_alloc(limits,(ptw->ptdw->ap_size+1)*sizeof(double),pth->error_message);
  limits[0]=mz_output[0]; limits[ptw->ptdw->ap_size]=mz_output[ptw->Nz_tot-1];
  for(int i=0;i<ptw->ptdw->ap_size-1;i++)limits[i+1]=-ptw->ptdw->ap_z_limits[i];

  solve_interposed=1;
  for(int interval=0;interval<ptw->ptdw->ap_size;interval++){
    ptw->ptdw->ap_current=interval;
    class_call(thermodynamics_vector_init(ppr,pba,pth,limits[interval],ptw),
               pth->error_message,pth->error_message);
    class_call(background_at_z(pba,-limits[interval],normal_info,inter_normal,
                               &(ptw->last_index_back),pvecback),
               pba->error_message,pth->error_message);

    if(interval==ptw->ptdw->index_ap_frec){
      if(!(limits[interval] < Q052_MZ_EVENT && Q052_MZ_EVENT < limits[interval+1])){
        snprintf(pth->error_message,_ERRORMSGSIZE_,"Q052_Z810_NOT_INSIDE_FREC");return _FAILURE_;
      }
      intervention_active=0;
      class_call(evolve(generic_evolver,limits[interval],Q052_MZ_EVENT,mz_output,pth->tt_size,&tpaw),
                 pth->error_message,pth->error_message);
      write_start(&tpaw,Q052_MZ_EVENT);
      intervention_active=1;
      enforce_q(&tpaw,ptw->ptdw->ptv->y);
      class_call(evolve(generic_evolver,Q052_MZ_EVENT,limits[interval+1],mz_output,pth->tt_size,&tpaw),
                 pth->error_message,pth->error_message);
    } else {
      if(intervention_active) enforce_q(&tpaw,ptw->ptdw->ptv->y);
      class_call(evolve(generic_evolver,limits[interval],limits[interval+1],mz_output,pth->tt_size,&tpaw),
                 pth->error_message,pth->error_message);
    }
  }

  if(pth->reio_z_or_tau==reio_z){
    class_call(thermodynamics_reionization_get_tau(ppr,pba,pth,ptw),
               pth->error_message,pth->error_message);
    pth->tau_reio=ptw->reionization_optical_depth;
  }
  if(ptw->ptdw->ap_size!=0)
    class_call(thermodynamics_vector_free(ptw->ptdw->ptv),pth->error_message,pth->error_message);
  free(limits);free(mz_output);
  return _SUCCESS_;
}

static void effective(struct background *ba,struct thermodynamics *th){
  FILE *f=open_out("effective_identity.json","wx");
  fputs("{\"schema\":\"Q052_EFFECTIVE_IDENTITY_V1\",\"program_id\":\"" Q052_ID "\",\"arm\":",f);js(f,arm);
  fputs(",\"mode\":",f);js(f,mode);fputs(",\"fields\":{",f);
  fputs("\"H0\":",f);jhex(f,ba->H0);fputs(",\"K\":",f);jhex(f,ba->K);
  fputs(",\"Omega0_b\":",f);jhex(f,ba->Omega0_b);fputs(",\"Omega0_cdm\":",f);jhex(f,ba->Omega0_cdm);
  fputs(",\"Omega0_g\":",f);jhex(f,ba->Omega0_g);fputs(",\"Omega0_lambda\":",f);jhex(f,ba->Omega0_lambda);
  fputs(",\"Omega0_ur\":",f);jhex(f,ba->Omega0_ur);fputs(",\"T_cmb\":",f);jhex(f,ba->T_cmb);
  fputs("},\"z_reio\":",f);jhex(f,th->z_reio);fputs(",\"tau_reio_output\":",f);jhex(f,th->tau_reio);
  fprintf(f,",\"reio_z_or_tau\":%d,\"solve_interposed\":%s,\"start_written\":%s}\n",
          th->reio_z_or_tau,solve_interposed?"true":"false",start_written?"true":"false");
  close_ok(f);
}

static void history(struct thermodynamics *th){
  /* Recompute the same eta-spline coefficients used for dkappa integration. */
  if(array_spline_table_line_to_line(th->tau_table,th->tt_size,th->thermodynamics_table,
      th->th_size,th->index_th_dkappa,th->index_th_dddkappa,_SPLINE_EST_DERIV_,th->error_message)==_FAILURE_)
    die("DKAPPA_SPLINE");
  FILE *f=open_out("history.csv","wx");
  fputs("z,eta_Mpc,xe,d2xe_dz2,dkappa_per_Mpc,dkappa_eta_second,cumulative_tau_T\n",f);
  double cum=0.;
  for(int i=0;i<th->tt_size;i++){
    double z=th->z_table[i];
    if(z>Q052_Z_EVENT+1e-12)break;
    double xe=th->thermodynamics_table[i*th->th_size+th->index_th_xe];
    double d2xe=th->d2thermodynamics_dz2_table[i*th->th_size+th->index_th_xe];
    double dk=th->thermodynamics_table[i*th->th_size+th->index_th_dkappa];
    double m=th->thermodynamics_table[i*th->th_size+th->index_th_dddkappa];
    fprintf(f,"%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g\n",z,th->tau_table[i],xe,d2xe,dk,m,cum);
    if(i+1<th->tt_size && th->z_table[i+1]<=Q052_Z_EVENT+1e-12){
      double h=th->tau_table[i+1]-th->tau_table[i];
      double dk1=th->thermodynamics_table[(i+1)*th->th_size+th->index_th_dkappa];
      double m1=th->thermodynamics_table[(i+1)*th->th_size+th->index_th_dddkappa];
      if(!(h<0.)||!isfinite(h)||!isfinite(dk)||!isfinite(dk1)||!isfinite(m)||!isfinite(m1))die("TAU_INTERVAL");
      cum -= h*(dk+dk1)/2. - h*h*h*(m+m1)/24.;
    }
  }
  close_ok(f);
}

int main(int argc,char **argv){
  struct precision pr;struct background ba;struct thermodynamics th;struct perturbations pt;
  struct primordial pm;struct fourier fo;struct transfer tr;struct harmonic hr;
  struct lensing le;struct distortions sd;struct output op;ErrorMsg err;
  outdir=getenv("Q052_NATIVE_OUT");arm=getenv("Q052_ARM");mode=getenv("Q052_MODE");run_id=getenv("Q052_RUN_ID");
  if(argc!=2||!outdir||!arm||!mode||!run_id||sizeof(double)!=8||DBL_MANT_DIG!=53||FLT_RADIX!=2||fegetround()!=FE_TONEAREST)return 2;
  if(strcmp(arm,"L")==0)q_xHeII=1e-6;else if(strcmp(arm,"R")==0)q_xHeII=0.;else return 3;
  if(strcmp(mode,"nominal")&&strcmp(mode,"refined"))return 4;
  if(input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err))die(err);
  if(ba.shooting_failed)die("BACKGROUND_SHOOTING_FAILED");
  if(background_init(&pr,&ba))die(ba.error_message);
  if(thermodynamics_init(&pr,&ba,&th))die(th.error_message);
  if(!solve_interposed||!start_written)die("INTERPOSITION_GATE");
  effective(&ba,&th);
  history(&th);
  FILE *f=open_out("runtime_result.json","wx");
  fputs("{\"schema\":\"Q052_NATIVE_RUNTIME_RESULT_V1\",\"program_id\":\"" Q052_ID "\",\"run_id\":",f);js(f,run_id);
  fputs(",\"arm\":",f);js(f,arm);fputs(",\"mode\":",f);js(f,mode);
  fprintf(f,",\"tol_scale\":%.17g,\"stepsize_scale\":%.17g,\"source_commit\":\"5a131c91d657dd9a7c6364cc45b038710f8d0d97\",\"execution_status\":\"COMPLETE\"}\n",tol_scale(),step_scale());
  close_ok(f);
  if(thermodynamics_free(&th)||background_free(&ba))die("FREE");
  puts("Q052_NATIVEPAIR_BRANCH_COMPLETE");
  return 0;
}
