/* Q-042 / V26: new numerical diagnostic lineage; unchanged cached CLASS core.
 * Link to the hash-pinned original classy.so. Never return an inferred history.
 * The tau-search entry is replaced by raw acquisition and process termination.
 */
#define _POSIX_C_SOURCE 200809L
#include "class.h"
#include "wrap_hyrec.h"
#include "q042_reference_integrators_v26.h"
#include <dlfcn.h>
#include <errno.h>
#include <signal.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define Q042_ID "Q042-REFACQ-V26"
#define Q042_BRANCH_CALL_CAP 1200000UL
#define Q042_GLOBAL_CALL_CAP 14400000UL
#define Q042_BRANCH_SECONDS 90.
#define Q042_CAMPAIGN_SECONDS 1400.

typedef int (*q042_derivs_fn)(double,double*,double*,void*,ErrorMsg);
static q042_derivs_fn q042_original_derivs;
static const char *q042_dir,*q042_run,*q042_config;
static double q042_started;
static unsigned q042_tau_entries;
static double *q042_state_D,*q042_state_H,*q042_state_He,*q042_state_xn,*q042_state_xr;
static int q042_states_size;
typedef struct {
 struct thermodynamics_parameters_and_workspace *a;
 double helium,wrapper_fHe,deadline,last_s,last_y[2],last_xn,last_xr,last_raw_s,last_raw_y[3],last_raw_dy[3];
 unsigned long calls,call_cap;
 const char *branch;
} q042_physical_context;
static q042_physical_context *q042_active;

static double q042_now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (double)t.tv_sec+1e-9*t.tv_nsec;}
static void *q042_original(const char *name){void *p=dlsym(RTLD_NEXT,name);if(!p){fprintf(stderr,"Q042_ORIGINAL_SYMBOL_GATE=FAIL %s %s\n",name,dlerror());exit(90);}return p;}
static void q042_number(FILE *f,double x){if(isnan(x))fputs("\"NaN\"",f);else if(isinf(x))fputs(x>0?"\"Infinity\"":"\"-Infinity\"",f);else fprintf(f,"%.17g",x);}
static void q042_string(FILE *f,const char *s){fputc('"',f);for(;*s;s++){unsigned char c=(unsigned char)*s;if(c=='"'||c=='\\')fprintf(f,"\\%c",c);else if(c<32)fprintf(f,"\\u%04x",c);else fputc(c,f);}fputc('"',f);}
static FILE *q042_open(const char *name,const char *mode){char p[4096];if(snprintf(p,sizeof p,"%s/%s",q042_dir,name)>=(int)sizeof p)return NULL;return fopen(p,mode);}
static void q042_identity(FILE *f,const char *branch){
 fputs("{\"q\":\"Q-042\",\"program_id\":\"" Q042_ID "\",\"run_id\":",f);q042_string(f,q042_run);
 fputs(",\"config_sha256\":",f);q042_string(f,q042_config);fputs(",\"branch_id\":",f);q042_string(f,branch);
 fputs(",\"result_status\":\"RAW_NOT_QUALIFIED\",\"scientific_result\":false",f);
}
static int q042_eligible(struct thermodynamics_parameters_and_workspace *a,double h0){
 struct thermo_diffeq_workspace *d=a->ptw->ptdw;
 if(a->pth->recombination!=hyrec||a->pth->has_exotic_injection||a->pth->has_varconst||a->pba->has_idm||a->pba->has_idr||a->pth->has_idm_b)return 0;
 if(!d->phyrec||!d->phyrec->data||!d->phyrec->data->cosmo)return 0;
 double f=d->phyrec->data->cosmo->fHe,limit=d->phyrec->xHeII_limit;
 return isfinite(f)&&isfinite(h0)&&f==a->ptw->fHe&&f>=0&&h0>=0&&limit==1e-6&&f*h0<limit;
}

int thermodynamics_derivs(double s,double *y,double *dy,void *workspace,ErrorMsg err){
 if(!q042_original_derivs)q042_original_derivs=(q042_derivs_fn)q042_original("thermodynamics_derivs");
 if(q042_active){
  q042_physical_context *c=q042_active;struct thermo_diffeq_workspace *d=c->a->ptw->ptdw;
  if(workspace!=c->a||d->ap_current!=d->index_ap_reio||d->require_He!=_FALSE_||d->require_H!=_TRUE_||y[d->ptv->index_ti_x_He]!=c->helium){snprintf(err,_ERRORMSGSIZE_,"Q042_IMMUTABLE_PHASE_GATE=FAIL");return _FAILURE_;}
  if(c->calls>=c->call_cap||q042_now()>c->deadline){snprintf(err,_ERRORMSGSIZE_,"Q042_BRANCH_RESOURCE_CAP");return _FAILURE_;}
  c->calls++;
  for(int j=0;j<d->ptv->ti_size;j++)dy[j]=0.; /* explicit inactive derivative; source finally negates */
 }
 int status=q042_original_derivs(s,y,dy,workspace,err);
 if(q042_active){
  q042_active->last_raw_s=s;for(int j=0;j<3;j++){q042_active->last_raw_y[j]=y[j];q042_active->last_raw_dy[j]=dy[j];}
  struct thermo_diffeq_workspace *d=q042_active->a->ptw->ptdw;
  q042_active->last_xn=d->x_noreio;q042_active->last_xr=d->x_reio;
  if(status==_SUCCESS_){
   for(int j=0;j<d->ptv->ti_size;j++)if(!isfinite(dy[j])){snprintf(err,_ERRORMSGSIZE_,"Q042_NONFINITE_DERIVATIVE");return _FAILURE_;}
   if(dy[d->ptv->index_ti_x_He]!=0.){snprintf(err,_ERRORMSGSIZE_,"Q042_INACTIVE_DYHE_GATE=FAIL");return _FAILURE_;}
  }
 }
 return status;
}

static int q042_physical_rhs(double s,const double y[2],double f[2],void *workspace,char *err,size_t n){
 q042_physical_context *c=workspace;struct thermo_vector *v=c->a->ptw->ptdw->ptv;
 double full[3]={0},dy[3]={0};ErrorMsg msg;f[0]=f[1]=NAN;
 full[v->index_ti_D_Tmat]=y[0];full[v->index_ti_x_H]=y[1];full[v->index_ti_x_He]=c->helium;
 if(thermodynamics_derivs(s,full,dy,c->a,msg)==_FAILURE_){snprintf(err,n,"%s",msg);return 1;}
 f[0]=dy[v->index_ti_D_Tmat];f[1]=dy[v->index_ti_x_H];return 0;
}

static int q042_states_allocate(int n){
 if(q042_states_size)return q042_states_size==n?0:1;
 q042_state_D=malloc((size_t)n*sizeof(double));q042_state_H=malloc((size_t)n*sizeof(double));q042_state_He=malloc((size_t)n*sizeof(double));q042_state_xn=malloc((size_t)n*sizeof(double));q042_state_xr=malloc((size_t)n*sizeof(double));
 if(!q042_state_D||!q042_state_H||!q042_state_He||!q042_state_xn||!q042_state_xr)return 1;
 q042_states_size=n;for(int j=0;j<n;j++)q042_state_D[j]=q042_state_H[j]=q042_state_He[j]=q042_state_xn[j]=q042_state_xr[j]=NAN;return 0;
}
int thermodynamics_sources(double s,double *y,double *dy,int index_z,void *workspace,ErrorMsg err){
 typedef int (*fn)(double,double*,double*,int,void*,ErrorMsg);static fn call;
 if(!call)call=(fn)q042_original("thermodynamics_sources");
 struct thermodynamics_parameters_and_workspace *a=workspace;int row=a->pth->tt_size-index_z-1;
 if(q042_states_allocate(a->pth->tt_size)){snprintf(err,_ERRORMSGSIZE_,"Q042_STATE_ALLOCATION_GATE=FAIL");return _FAILURE_;}
 int status=call(s,y,dy,index_z,workspace,err);
 if(status==_SUCCESS_&&row>=0&&row<q042_states_size){
  struct thermo_diffeq_workspace *d=a->ptw->ptdw;
  q042_state_D[row]=y[d->ptv->index_ti_D_Tmat];q042_state_H[row]=q042_active?y[d->ptv->index_ti_x_H]:d->x_H;q042_state_He[row]=q042_active?q042_active->helium:d->x_He;
  q042_state_xn[row]=q042_active?q042_active->last_xn:d->x_noreio;q042_state_xr[row]=q042_active?q042_active->last_xr:d->x_reio;
 }
 return status;
}

static int q042_adapter_preflight(struct thermodynamics_parameters_and_workspace *a,double s,char *err,size_t n){
 struct thermo_diffeq_workspace *d=a->ptw->ptdw;struct thermo_vector *v=d->ptv;
 if(v->ti_size!=3||v->index_ti_D_Tmat!=0||v->index_ti_x_He!=1||v->index_ti_x_H!=2||d->ap_current!=d->index_ap_reio||q042_states_size!=a->pth->tt_size||!q042_eligible(a,v->y[v->index_ti_x_He])){snprintf(err,n,"Q042_ELIGIBILITY_VECTOR_OR_PREFIX_CAPTURE_GATE=FAIL");return 1;}
 for(int j=0;j<3;j++)if(!isfinite(v->y[j])){snprintf(err,n,"Q042_NONFINITE_ACCEPTED_ENTRY");return 1;}
 q042_physical_context c={0};c.a=a;c.helium=v->y[v->index_ti_x_He];c.wrapper_fHe=d->phyrec->data->cosmo->fHe;c.deadline=q042_now()+10;c.call_cap=100;c.branch="PREFLIGHT";
 double original_dy[3],reduced_dy[3];ErrorMsg msg;
 if(!q042_original_derivs)q042_original_derivs=(q042_derivs_fn)q042_original("thermodynamics_derivs");
 FILE *samples=q042_open("adapter_samples.jsonl","w");if(!samples){snprintf(err,n,"Q042_ADAPTER_SAMPLE_OUTPUT=FAIL");return 1;}
 for(int probe=0;probe<3;probe++){
  double y[3]={v->y[0],v->y[1],v->y[2]};y[0]+=(probe==1?.001:0.);y[2]+=(probe==2?1e-8:0.);
  for(int j=0;j<3;j++)original_dy[j]=reduced_dy[j]=NAN;
  d->require_H=_TRUE_;d->require_He=_TRUE_;
  int original_status=q042_original_derivs(s,y,original_dy,a,msg);
  d->require_He=_FALSE_;q042_active=&c;
  int status=original_status==_SUCCESS_?thermodynamics_derivs(s,y,reduced_dy,a,msg):_FAILURE_;q042_active=NULL;
  q042_identity(samples,"PREFLIGHT");fprintf(samples,",\"probe\":%d,\"s\":%.17g,\"y_D_He_H\":[",probe,s);
  for(int j=0;j<3;j++){if(j)fputc(',',samples);q042_number(samples,y[j]);}fputs("],\"original_dy\":[",samples);
  for(int j=0;j<3;j++){if(j)fputc(',',samples);q042_number(samples,original_dy[j]);}fputs("],\"reduced_dy\":[",samples);
  for(int j=0;j<3;j++){if(j)fputc(',',samples);q042_number(samples,reduced_dy[j]);}fprintf(samples,"],\"original_status\":%d,\"reduced_status\":%d}\n",original_status,status);fflush(samples);
  if(status==_FAILURE_||!isfinite(original_dy[0])||!isfinite(original_dy[2])||original_dy[0]!=reduced_dy[0]||original_dy[2]!=reduced_dy[2]||original_dy[1]!=0.||reduced_dy[1]!=0.){snprintf(err,n,"Q042_REDUCED_RHS_COMPARISON=FAIL probe=%d %.1850s",probe,status==_FAILURE_?msg:"finite derivatives differ");fclose(samples);return 1;}
 }
 fclose(samples);
 return 0;
}

static int q042_export_table(struct thermodynamics_parameters_and_workspace *a,const char *branch,char *err,size_t n){
 char name[160];snprintf(name,sizeof name,"%s_nodes.csv",branch);FILE *f=q042_open(name,"w");if(!f){snprintf(err,n,"Q042_NODE_OUTPUT_OPEN=FAIL");return 1;}
 struct thermodynamics *th=a->pth;
 fputs("q,program_id,run_id,branch_id,config_sha256,scope,z,eta_Mpc,D_Tmat_K,x_H,x_He,x_noreio,x_reio_rhs,xe_source,dkappa_per_Mpc,dddkappa_eta\n",f);
 for(int i=0;i<th->tt_size;i++){
  const char *scope=th->z_table[i]<=a->ppr->reionization_z_start_max?(isfinite(q042_state_H[i])?"ACQUIRED_REIONIZATION":"NOT_ACQUIRED"):"SHARED_RECOMBINATION_PREFIX";
  if(strcmp(branch,"SHARED_PREFIX")==0&&strcmp(scope,"ACQUIRED_REIONIZATION")==0)scope="SHARED_ENTRY_BOUNDARY";
  fprintf(f,"Q-042," Q042_ID ",%s,%s,%s,%s",q042_run,branch,q042_config,scope);
  double x[10]={th->z_table[i],th->tau_table[i],q042_state_D[i],q042_state_H[i],q042_state_He[i],q042_state_xn[i],q042_state_xr[i],th->thermodynamics_table[i*th->th_size+th->index_th_xe],th->thermodynamics_table[i*th->th_size+th->index_th_dkappa],th->thermodynamics_table[i*th->th_size+th->index_th_dddkappa]};
  for(int j=0;j<10;j++){fputc(',',f);if(j==9&&!isfinite(x[j]))fputs("NOT_COMPUTED",f);else q042_number(f,x[j]);}fputc('\n',f);
 }
 int failed=ferror(f);if(fclose(f))failed=1;if(failed){snprintf(err,n,"Q042_NODE_OUTPUT_WRITE=FAIL");return 1;}return 0;
}

static int q042_tau(struct thermodynamics_parameters_and_workspace *a,double *tau,double *legacy,int *k,int *N,char *err,size_t n){
 struct thermodynamics *th=a->pth;double minimum=HUGE_VAL;
 *k=0;*N=0;*tau=*legacy=0.;
 for(int i=0;i<th->tt_size;i++){
  double xe=th->thermodynamics_table[i*th->th_size+th->index_th_xe],dk=th->thermodynamics_table[i*th->th_size+th->index_th_dkappa];
  if(!isfinite(xe)||!isfinite(dk)||!isfinite(th->tau_table[i])){snprintf(err,n,"Q042_NONFINITE_FULL_NODE_TABLE row=%d",i);return 1;}
  if(i<th->tt_size-1&&xe<minimum){minimum=xe;*k=i;}
 }
 if(*k==0)return 0;
 *N=*k<3?3:*k;
 if(array_spline_table_line_to_line(th->tau_table,*N,th->thermodynamics_table,th->th_size,th->index_th_dkappa,th->index_th_dddkappa,_SPLINE_EST_DERIV_,th->error_message)==_FAILURE_){snprintf(err,n,"Q042_SPLINE_COEFFICIENT_GATE=FAIL %.1900s",th->error_message);return 1;}
 double sum=0.,old=0.;
 for(int i=0;i<*N-1;i++){
  double h=th->tau_table[i+1]-th->tau_table[i],y0=th->thermodynamics_table[i*th->th_size+th->index_th_dkappa],y1=th->thermodynamics_table[(i+1)*th->th_size+th->index_th_dkappa];
  double m=th->thermodynamics_table[i*th->th_size+th->index_th_dddkappa]+th->thermodynamics_table[(i+1)*th->th_size+th->index_th_dddkappa];
  if(!isfinite(h)||!isfinite(m)||h>=0){snprintf(err,n,"Q042_CONFORMAL_SPLINE_GATE=FAIL");return 1;}
  sum+=h*(y0+y1)/2.-h*h*h*m/24.;old+=h*(y0+y1)/2.+h*h*h*m/24.;
 }
 *tau=-sum;*legacy=-old;
 if(!isfinite(*tau)||!isfinite(*legacy)){snprintf(err,n,"Q042_NONFINITE_SPLINE_INTEGRAL");return 1;}return 0;
}

static void q042_branch_result(const char *branch,const char *status,const char *error,q042_physical_context *c,q042_solver_stats *st,int outputs,double tau,double legacy,int k,int N){
 char name[160];snprintf(name,sizeof name,"%s_result.json",branch);FILE *f=q042_open(name,"w");if(!f)return;
 q042_identity(f,branch);fputs(",\"execution_status\":",f);q042_string(f,status);fputs(",\"error\":",f);q042_string(f,error);
 fprintf(f,",\"rhs_calls\":%lu,\"kernel_rhs_calls\":%lu,\"steps\":%lu,\"max_newton_used\":%d,\"native_outputs_written\":%d,\"minimum_row\":%d,\"effective_n\":%d,\"last_accepted_s\":",c?c->calls:0,st?st->rhs_calls:0,st?st->steps:0,st?st->max_newton_used:0,outputs,k,N);
 q042_number(f,c?c->last_s:NAN);fputs(",\"last_accepted_y\":[",f);q042_number(f,c?c->last_y[0]:NAN);fputc(',',f);q042_number(f,c?c->last_y[1]:NAN);
 fputs("],\"tau_correct_same_spline\":",f);q042_number(f,tau);fputs(",\"tau_legacy_same_coefficients\":",f);q042_number(f,legacy);
 fputs(",\"legacy_minus_correct\":",f);q042_number(f,legacy-tau);
 fputs(",\"last_kernel_evaluation\":{\"s\":",f);q042_number(f,st?st->last_s:NAN);
 fputs(",\"y\":[",f);q042_number(f,st?st->last_y[0]:NAN);fputc(',',f);q042_number(f,st?st->last_y[1]:NAN);
 fputs("],\"rhs\":[",f);q042_number(f,st?st->last_f[0]:NAN);fputc(',',f);q042_number(f,st?st->last_f[1]:NAN);fputs("]}",f);
 fputs(",\"last_original_derivative_call\":{\"s\":",f);q042_number(f,c?c->last_raw_s:NAN);fputs(",\"y_D_He_H\":[",f);
 for(int j=0;j<3;j++){if(j)fputc(',',f);q042_number(f,c?c->last_raw_y[j]:NAN);}fputs("],\"dy_D_He_H\":[",f);
 for(int j=0;j<3;j++){if(j)fputc(',',f);q042_number(f,c?c->last_raw_dy[j]:NAN);}fputs("]}",f);
 fprintf(f,",\"max_accepted_newton_scaled_residual\":%.17g,\"history_accuracy_qualified\":false,\"prediction_likelihood_qualified\":false}\n",st?st->max_scaled_residual:0.);fclose(f);
}

static int q042_run_branch(struct thermodynamics_parameters_and_workspace *a,double ini,double end,double *grid,int size,int trial,int method,int sub,const char *branch,unsigned long cap){
 struct thermo_diffeq_workspace *d=a->ptw->ptdw;struct thermo_vector *v=d->ptv;struct thermo_reionization_parameters *rp=a->ptw->ptrp;
 q042_physical_context c={0};q042_solver_stats stats={0};char err[_ERRORMSGSIZE_]="";int written=0,k=-1,N=-1;double tau=NAN,legacy=NAN;
 c.a=a;c.helium=v->y[v->index_ti_x_He];c.wrapper_fHe=d->phyrec->data->cosmo->fHe;c.deadline=fmin(q042_now()+Q042_BRANCH_SECONDS,q042_started+Q042_CAMPAIGN_SECONDS);c.call_cap=cap;c.branch=branch;
 double s=ini,y[2]={v->y[v->index_ti_D_Tmat],v->y[v->index_ti_x_H]};c.last_s=s;c.last_y[0]=y[0];c.last_y[1]=y[1];
 double center=trial?0.:a->ppr->reionization_z_start_max-a->ppr->reionization_start_factor*a->pth->reionization_width;
 double start=trial?fmax(a->ppr->reionization_start_factor*a->pth->reionization_width,a->pth->helium_fullreio_redshift+a->ppr->reionization_start_factor*a->pth->helium_fullreio_width):a->ppr->reionization_z_start_max;
 rp->reionization_parameters[rp->index_re_reio_redshift]=center;rp->reionization_parameters[rp->index_re_reio_start]=start;
 d->require_H=_TRUE_;d->require_He=_FALSE_;q042_active=&c;
 char name[160];snprintf(name,sizeof name,"%s_defects.csv",branch);FILE *def=q042_open(name,"w");
 snprintf(name,sizeof name,"%s_accepted_nodes.csv",branch);FILE *stream=q042_open(name,"w");
 if(!def||!stream){snprintf(err,sizeof err,"Q042_STREAM_OUTPUT_OPEN=FAIL");goto failed;}
 fputs("q,program_id,run_id,branch_id,config_sha256,s_mid,h,defect_D_Tmat,defect_x_H,s_right,D_Tmat_right,x_H_right\n",def);
 fputs("q,program_id,run_id,branch_id,config_sha256,native_row,z,eta_Mpc,D_Tmat,x_H,x_He,x_noreio,x_reio_rhs,xe_source,dkappa_per_Mpc,rhs_calls\n",stream);
 /* Coefficient scratch outside the used support is explicitly uncomputed. */
 for(int i=0;i<a->pth->tt_size;i++){
  a->pth->thermodynamics_table[i*a->pth->th_size+a->pth->index_th_dddkappa]=NAN;
  if(a->pth->z_table[i]<=a->ppr->reionization_z_start_max)q042_state_D[i]=q042_state_H[i]=q042_state_He[i]=q042_state_xn[i]=q042_state_xr[i]=NAN;
 }
 for(int i=0;i<size;i++){
  double target=grid[i];if(target<ini)continue;if(target>end)break;
  double h=(target-s)/sub;
  if(h<0||!isfinite(h)){snprintf(err,sizeof err,"Q042_NATIVE_GRID_ORDER_GATE=FAIL");goto failed;}
  for(int j=0;j<sub&&h>0;j++){
   double next[2];
   if(q042_step(method,s,h,y,next,q042_physical_rhs,&c,&stats,err,sizeof err))goto failed;
   /* Hermite midpoint defect of THIS measured step: point diagnostic only. */
   double f0[2],f1[2],dense[2],dense_prime[2],fm[2];
   if(q042_eval(q042_physical_rhs,s,y,f0,&c,&stats,err,sizeof err)||q042_eval(q042_physical_rhs,s+h,next,f1,&c,&stats,err,sizeof err))goto failed;
   for(int b=0;b<2;b++){dense[b]=.5*(y[b]+next[b])+h*(f0[b]-f1[b])/8.;dense_prime[b]=1.5*(next[b]-y[b])/h-.25*(f0[b]+f1[b]);}
   if(q042_eval(q042_physical_rhs,s+.5*h,dense,fm,&c,&stats,err,sizeof err))goto failed;
   fprintf(def,"Q-042," Q042_ID ",%s,%s,%s,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g\n",q042_run,branch,q042_config,s+.5*h,h,dense_prime[0]-fm[0],dense_prime[1]-fm[1],s+h,next[0],next[1]);fflush(def);
   s+=h;y[0]=next[0];y[1]=next[1];c.last_s=s;c.last_y[0]=y[0];c.last_y[1]=y[1];
  }
  s=target;c.last_s=s;
  double full[3]={0},dy[3]={0};full[v->index_ti_D_Tmat]=y[0];full[v->index_ti_x_H]=y[1];full[v->index_ti_x_He]=c.helium;
  unsigned long before_source=c.calls;
  if(thermodynamics_sources(s,full,dy,i,a,err)==_FAILURE_)goto failed;
  if(c.calls!=before_source+1){snprintf(err,sizeof err,"Q042_DERIVS_INTERPOSITION_GATE=FAIL");goto failed;}
  int row=a->pth->tt_size-i-1;struct thermodynamics *th=a->pth;
  fprintf(stream,"Q-042," Q042_ID ",%s,%s,%s,%d,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%lu\n",q042_run,branch,q042_config,row,th->z_table[row],th->tau_table[row],y[0],y[1],c.helium,c.last_xn,c.last_xr,th->thermodynamics_table[row*th->th_size+th->index_th_xe],th->thermodynamics_table[row*th->th_size+th->index_th_dkappa],c.calls);fflush(stream);
  if(ferror(stream)||ferror(def)){snprintf(err,sizeof err,"Q042_STREAM_OUTPUT_WRITE=FAIL");goto failed;}
  written++;
 }
 if(s!=end||written==0){snprintf(err,sizeof err,"Q042_NATIVE_OUTPUT_COMPLETENESS_GATE=FAIL");goto failed;}
 if(q042_tau(a,&tau,&legacy,&k,&N,err,sizeof err))goto failed;
 if(q042_export_table(a,branch,err,sizeof err))goto failed;
 q042_active=NULL;if(def)fclose(def);if(stream)fclose(stream);q042_branch_result(branch,"COMPLETE","",&c,&stats,written,tau,legacy,k,N);return 0;
 failed:
 q042_active=NULL;if(def)fclose(def);if(stream)fclose(stream);
 /* Partial table is RAW; source below last accepted node may be unfilled. */
 char output_error[256];q042_export_table(a,branch,output_error,sizeof output_error);
 q042_branch_result(branch,"FAILED",err,&c,&stats,written,tau,legacy,k,N);return 1;
}

int thermodynamics_reionization_evolve_with_tau(struct thermodynamics_parameters_and_workspace *a,double ini,double end,double *grid,int size){
 q042_tau_entries++;char err[_ERRORMSGSIZE_]="";
 if(q042_tau_entries!=1||a->pth->reio_parametrization!=reio_camb||a->pth->reio_z_or_tau!=reio_tau||ini!=-50.||end!=0.||size!=a->pth->tt_size||q042_adapter_preflight(a,ini,err,sizeof err)){
  fprintf(stderr,"Q042_ACQUISITION_PREFLIGHT=FAIL %s\n",err);exit(91);
 }
 struct thermo_vector *v=a->ptw->ptdw->ptv;FILE *entry=q042_open("accepted_entry.json","w");if(!entry)exit(92);
 int archived_equal=v->y[v->index_ti_D_Tmat]==-86.955287923490403&&v->y[v->index_ti_x_H]==.00024187860481588748&&v->y[v->index_ti_x_He]==1.2261504557092879e-5&&a->ptw->fHe==.081556058814182833&&a->ptw->Tcmb==2.7254999999999998;
 printf("Q042_ARCHIVED_ENTRY_COMPARISON=%s; actual entry recorded before any trial integration\n",archived_equal?"EXACT":"DIFFERENT_SHARED_CONDITIONING_RECORDED");
 q042_identity(entry,"SHARED_ENTRY");fprintf(entry,",\"source_rhs_comparison\":\"PASS\",\"tau_search_executed\":false,\"mz_ini\":%.17g,\"mz_end\":%.17g,\"grid_size\":%d,\"fHe\":%.17g,\"wrapper_fHe\":%.17g,\"cutoff\":%.17g,\"D_Tmat\":%.17g,\"x_H\":%.17g,\"x_He\":%.17g,\"Tcmb\":%.17g,\"SIunit_nH0\":%.17g,\"original_tau_reio\":%.17g,\"reionization_width\":%.17g,\"reionization_exponent\":%.17g,\"reionization_start_factor\":%.17g,\"helium_fullreio_redshift\":%.17g,\"helium_fullreio_width\":%.17g}\n",ini,end,size,a->ptw->fHe,a->ptw->ptdw->phyrec->data->cosmo->fHe,a->ptw->ptdw->phyrec->xHeII_limit,v->y[v->index_ti_D_Tmat],v->y[v->index_ti_x_H],v->y[v->index_ti_x_He],a->ptw->Tcmb,a->ptw->SIunit_nH0,a->pth->tau_reio,a->pth->reionization_width,a->pth->reionization_exponent,a->ppr->reionization_start_factor,a->pth->helium_fullreio_redshift,a->pth->helium_fullreio_width);fclose(entry);
 FILE *geometry=q042_open("accepted_grid.csv","w");if(!geometry)exit(93);
 fputs("q,program_id,run_id,config_sha256,row,z,eta_Mpc,mz_output_by_index\n",geometry);
 for(int i=0;i<size;i++)fprintf(geometry,"Q-042," Q042_ID ",%s,%s,%d,%.17g,%.17g,%.17g\n",q042_run,q042_config,i,a->pth->z_table[i],a->pth->tau_table[i],grid[i]);
 fclose(geometry);
 for(int i=0;i<a->pth->tt_size;i++)a->pth->thermodynamics_table[i*a->pth->th_size+a->pth->index_th_dddkappa]=NAN;
 if(q042_export_table(a,"SHARED_PREFIX",err,sizeof err)){fprintf(stderr,"%s\n",err);exit(93);}
 FILE *plan=q042_open("native_branch_manifest.json","w");if(!plan)exit(93);q042_identity(plan,"MANIFEST");fputs(",\"expected_branches\":12,\"branches\":[",plan);fflush(NULL);
 unsigned long consumed=0;int count=0;
 for(int trial=0;trial<2;trial++)for(int method=0;method<2;method++)for(int sub=1;sub<=4;sub*=2){
  char branch[80];snprintf(branch,sizeof branch,"%s-%s-L%d",trial?"LOWER":"UPPER",method?"MIDPOINT":"RK4",sub);
  if(count++)fputc(',',plan);
  const char *parent_status="FAILED";int childcode=-1;
  if(q042_now()>q042_started+Q042_CAMPAIGN_SECONDS||consumed>=Q042_GLOBAL_CALL_CAP){
   parent_status="NOT_ATTEMPTED_RESOURCE_CAP";q042_branch_result(branch,parent_status,"Q042_GLOBAL_RESOURCE_CAP",NULL,NULL,0,NAN,NAN,-1,-1);
  }else{
   unsigned long cap=Q042_GLOBAL_CALL_CAP-consumed;if(cap>Q042_BRANCH_CALL_CAP)cap=Q042_BRANCH_CALL_CAP;
   fflush(NULL);pid_t pid=fork();
   if(pid==0){
    char name[160],path[4096];snprintf(name,sizeof name,"%s_native.log",branch);snprintf(path,sizeof path,"%s/%s",q042_dir,name);if(!freopen(path,"w",stdout)||!freopen(path,"a",stderr))_exit(94);
    q042_identity(stdout,branch);fputs(",\"kind\":\"BRANCH_LOG_HEADER\"}\n",stdout);fflush(stdout);
    int rc=q042_run_branch(a,ini,end,grid,size,trial,method,sub,branch,cap);fflush(NULL);_exit(rc);
   }
   if(pid<0){q042_branch_result(branch,"FAILED","Q042_FORK_GATE=FAIL",NULL,NULL,0,NAN,NAN,-1,-1);}
   else{
    int status=0;double until=fmin(q042_now()+Q042_BRANCH_SECONDS+2.,q042_started+Q042_CAMPAIGN_SECONDS+2.);int done=0;
    while(q042_now()<until){pid_t w=waitpid(pid,&status,WNOHANG);if(w==pid){done=1;break;}if(w<0){break;}struct timespec pause={0,10000000};nanosleep(&pause,NULL);}
    if(!done){kill(pid,SIGKILL);waitpid(pid,&status,0);q042_branch_result(branch,"FAILED","Q042_PARENT_WALL_CAP",NULL,NULL,0,NAN,NAN,-1,-1);consumed+=cap;}
    else if(WIFEXITED(status)){childcode=WEXITSTATUS(status);parent_status=childcode==0?"COMPLETE":"FAILED";
     /* Worst-case accounting deliberately reserves each attempted branch cap. */
     consumed+=cap;
    }else{q042_branch_result(branch,"FAILED","Q042_CHILD_SIGNAL",NULL,NULL,0,NAN,NAN,-1,-1);consumed+=cap;}
   }
  }
  fputs("{\"branch_id\":",plan);q042_string(plan,branch);fputs(",\"execution_status\":",plan);q042_string(plan,parent_status);fprintf(plan,",\"child_exit_code\":%d}",childcode);fflush(plan);
 }
 fprintf(plan,"],\"reserved_rhs_budget\":%lu,\"elapsed_seconds\":%.17g,\"history_accuracy_qualified\":false}\n",consumed,q042_now()-q042_started);fclose(plan);
 puts("Q042_RAW_ACQUISITION=ACCOUNTED_NO_INFERENCE_RESULT");fflush(NULL);exit(0);
}

#ifndef Q042_ADAPTER_FIXTURE
int main(int argc,char **argv){
 struct precision pr;struct background ba;struct thermodynamics th;struct perturbations pt;struct primordial pm;struct fourier fo;struct transfer tr;struct harmonic hr;struct lensing le;struct distortions sd;struct output op;ErrorMsg err;
 q042_started=q042_now();q042_dir=getenv("Q042_REFACQ_DIR");q042_run=getenv("Q042_REFACQ_RUN");q042_config=getenv("Q042_REFACQ_CONFIG_SHA256");
 if(argc!=2||!q042_dir||!q042_run||!q042_config||strlen(q042_config)!=64){fprintf(stderr,"Q042_NATIVE_ARGUMENT_GATE=FAIL\n");return 2;}
 if(input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err)==_FAILURE_){fprintf(stderr,"Q042_INPUT_GATE=FAIL %s\n",err);return 3;}
 if(background_init(&pr,&ba)==_FAILURE_){fprintf(stderr,"Q042_BACKGROUND_GATE=FAIL %s\n",ba.error_message);return 4;}
 /* Unchanged prefix runs until the exported tau-entry boundary. No spectra. */
 if(thermodynamics_init(&pr,&ba,&th)==_FAILURE_){fprintf(stderr,"Q042_PREFIX_OR_PREFLIGHT_GATE=FAIL %s\n",th.error_message);return 5;}
 fprintf(stderr,"Q042_TAU_ENTRY_INTERPOSITION_GATE=FAIL no expected exit\n");return 6;
}
#endif
