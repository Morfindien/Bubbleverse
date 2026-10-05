#define Q042_ADAPTER_FIXTURE_GUARD_UNUSED 1
/* Q-042 / V27: fixed-state switch probes; unchanged cached CLASS core.
 * Link to the hash-pinned original classy.so. Never return an inferred history.
 * The tau-search entry is replaced by fixed-state measurement and process termination.
 */
#define _POSIX_C_SOURCE 200809L
#include "class.h"
#include "wrap_hyrec.h"
#include "q042_switch_anchors_v27.h"
#include <dlfcn.h>
#include <errno.h>
#include <signal.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define Q042_ID "Q042-SWITCHPROBE-V27"
#define Q042_BRANCH_CALL_CAP 64UL
#define Q042_GLOBAL_CALL_CAP 128UL
#define Q042_BRANCH_SECONDS 20.
#define Q042_CAMPAIGN_SECONDS 140.

typedef int (*q042_derivs_fn)(double,double*,double*,void*,ErrorMsg);
static q042_derivs_fn q042_original_derivs;
static const char *q042_dir,*q042_run,*q042_config;
static double q042_started;
static unsigned q042_tau_entries;
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

static int q042_adapter_preflight(struct thermodynamics_parameters_and_workspace *a,double s,char *err,size_t n){
 struct thermo_diffeq_workspace *d=a->ptw->ptdw;struct thermo_vector *v=d->ptv;
 if(v->ti_size!=3||v->index_ti_D_Tmat!=0||v->index_ti_x_He!=1||v->index_ti_x_H!=2||d->ap_current!=d->index_ap_reio||!q042_eligible(a,v->y[v->index_ti_x_He])){snprintf(err,n,"Q042_ELIGIBILITY_VECTOR_OR_PREFIX_CAPTURE_GATE=FAIL");return 1;}
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


static int kernel_model=-1,kernel_calls,hmla_calls,tla_calls,kernel_error;
static double kernel_TR,kernel_ratio;
double rec_dxHIIdlna(HYREC_DATA*data,int model,double xe,double xH,double nH,double H,double TM,double TR,unsigned iz,double z){
 typedef double (*fn)(HYREC_DATA*,int,double,double,double,double,double,double,unsigned,double);static fn call;
 if(!call)call=(fn)q042_original("rec_dxHIIdlna");
 kernel_calls++;kernel_model=model;kernel_TR=TR;kernel_ratio=TM/TR;
 double result=call(data,model,xe,xH,nH,H,TM,TR,iz,z);kernel_error=data->error;return result;
}
double rec_HMLA_dxHIIdlna(HYREC_DATA*data,double xe,double xH,double nH,double H,double TM,double TR){
 typedef double(*fn)(HYREC_DATA*,double,double,double,double,double,double);static fn call;
 if(!call){call=(fn)q042_original("rec_HMLA_dxHIIdlna");}
 hmla_calls++;return call(data,xe,xH,nH,H,TM,TR);
}
double rec_TLA_dxHIIdlna(REC_COSMOPARAMS*cosmo,double xe,double xH,double nH,double H,double TM,double TR,double fudge){
 typedef double(*fn)(REC_COSMOPARAMS*,double,double,double,double,double,double,double);static fn call;
 if(!call){call=(fn)q042_original("rec_TLA_dxHIIdlna");}
 tla_calls++;return call(cosmo,xe,xH,nH,H,TM,TR,fudge);
}
static int q042_probe_trial(struct thermodynamics_parameters_and_workspace*a,int trial){
 const char*name=trial?"LOWER":"UPPER";char file[80];snprintf(file,sizeof file,"%s_samples.jsonl",name);FILE*out=q042_open(file,"w");if(!out)return 1;
 struct thermo_diffeq_workspace*d=a->ptw->ptdw;struct thermo_reionization_parameters*rp=a->ptw->ptrp;
 q042_physical_context c={0};c.a=a;c.helium=Q042_ANCHORS[trial][1];c.branch=name;c.deadline=q042_now()+20.;c.call_cap=64;
 rp->reionization_parameters[rp->index_re_reio_redshift]=trial?0.:a->ppr->reionization_z_start_max-a->ppr->reionization_start_factor*a->pth->reionization_width;
 rp->reionization_parameters[rp->index_re_reio_start]=trial?fmax(a->ppr->reionization_start_factor*a->pth->reionization_width,a->pth->helium_fullreio_redshift+a->ppr->reionization_start_factor*a->pth->helium_fullreio_width):a->ppr->reionization_z_start_max;
 d->require_H=_TRUE_;d->require_He=_FALSE_;q042_active=&c;
 const double eps[3]={1e-6,1e-8,1e-10};double zstar=TR_MIN/(kBoltz*a->ptw->Tcmb)-1.;int failed=0;
 for(int order=0;order<2;order++)for(int ii=0;ii<3;ii++)for(int jj=0;jj<2;jj++){
  int i=order?2-ii:ii,side=order?(jj? -1:1):(jj?1:-1);double z=zstar+side*eps[i];
  double y[2]={Q042_ANCHORS[trial][0],Q042_ANCHORS[trial][2]},dy[2];char err[_ERRORMSGSIZE_]="";
  kernel_model=-1;kernel_calls=hmla_calls=tla_calls=kernel_error=0;kernel_TR=kernel_ratio=NAN;
  int status=q042_physical_rhs(-z,y,dy,&c,err,sizeof err);
  q042_identity(out,name);fprintf(out,",\"trial\":\"%s\",\"order\":%d,\"epsilon_index\":%d,\"epsilon\":%.17g,\"side\":%d,\"z\":%.17g,\"zstar\":%.17g,\"model\":%d,\"kernel_calls\":%d,\"hmla_calls\":%d,\"tla_calls\":%d,\"kernel_error\":%d,\"status\":%d,\"TR_eV\":",name,order,i,eps[i],side,z,zstar,kernel_model,kernel_calls,hmla_calls,tla_calls,kernel_error,status);q042_number(out,kernel_TR);
  fputs(",\"T_ratio\":",out);q042_number(out,kernel_ratio);fputs(",\"y\":[",out);
  for(int j=0;j<3;j++){if(j)fputc(',',out);q042_number(out,Q042_ANCHORS[trial][j]);}
  fputs("],\"dy\":[",out);q042_number(out,dy[0]);fputs(",0,",out);q042_number(out,dy[1]);fputs("],\"x_noreio\":",out);q042_number(out,c.last_xn);fputs(",\"x_reio_rhs\":",out);q042_number(out,c.last_xr);
  fputs(",\"error\":",out);q042_string(out,err);fputs("}\n",out);fflush(out);
  if(status||kernel_error||kernel_calls!=1||!isfinite(kernel_ratio)||ferror(out)){failed=1;goto done;}
 }
 done:q042_active=NULL;if(fclose(out))failed=1;return failed;
}
int thermodynamics_reionization_evolve_with_tau(struct thermodynamics_parameters_and_workspace*a,double ini,double end,double*grid,int size){
 (void)grid;q042_tau_entries++;char err[_ERRORMSGSIZE_]="";struct thermo_vector*v=a->ptw->ptdw->ptv;
 if(q042_now()-q042_started>120.||q042_tau_entries!=1||a->pth->reio_parametrization!=reio_camb||a->pth->reio_z_or_tau!=reio_tau||ini!=-50.||end!=0.||size!=a->pth->tt_size||q042_adapter_preflight(a,ini,err,sizeof err))exit(91);
 if(v->y[0]!=-86.955287923490403||v->y[1]!=1.2261504557092879e-5||v->y[2]!=.00024187860481588748||a->ptw->fHe!=.081556058814182833||a->ptw->Tcmb!=2.7254999999999998||TR_MIN!=.004||kBoltz!=8.617343e-5||MODEL!=SWIFT){fputs("Q042_FROZEN_ENTRY_OR_CONSTANT_GATE=FAIL\n",stderr);exit(92);}
 FILE*manifest=q042_open("native_trial_manifest.json","w");if(!manifest)exit(93);q042_identity(manifest,"MANIFEST");fputs(",\"expected_trials\":2,\"trials\":[",manifest);fflush(NULL);
 for(int t=0;t<2;t++){
  if(t){fputc(',',manifest);}
  int status=0,code=-1;fflush(NULL);pid_t child=fork();
  if(child==0){int rc=q042_probe_trial(a,t);fflush(NULL);_exit(rc);}
  if(child>0){double deadline=fmin(q042_now()+22.,q042_started+140.);int done=0;
   while(q042_now()<deadline){pid_t w=waitpid(child,&status,WNOHANG);if(w==child){done=1;break;}if(w<0)break;struct timespec pause={0,10000000};nanosleep(&pause,NULL);}
   if(!done){kill(child,SIGKILL);waitpid(child,&status,0);}else if(WIFEXITED(status))code=WEXITSTATUS(status);
  }
  fprintf(manifest,"{\"trial\":\"%s\",\"child_exit_code\":%d,\"execution_status\":\"%s\"}",t?"LOWER":"UPPER",code,code==0?"COMPLETE":"FAILED");fflush(manifest);
 }
 fputs("]}\n",manifest);fclose(manifest);exit(0);
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
