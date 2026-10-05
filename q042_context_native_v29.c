/* Q-042 / V29: original-context capture; reused V26 accepted-entry adapter.
 * Link to the hash-pinned original classy.so. Never return an inferred history.
 * The tau-search entry is replaced by raw acquisition and process termination.
 */
#define _POSIX_C_SOURCE 200809L
#include "class.h"
#include "wrap_hyrec.h"
#include <float.h>
#include <fenv.h>
#include <dlfcn.h>
#include <errno.h>
#include <signal.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define Q042_ID "Q042-CONTEXT-V29"
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


static void hx(FILE *f,double x){if(!isfinite(x)){fprintf(stderr,"NONFINITE_CONTEXT\n");exit(95);}fprintf(f,"\"%a\"",x);}
static void kv(FILE *f,const char *name,double x,int comma){if(comma)fputc(',',f);q042_string(f,name);fputc(':',f);hx(f,x);}
static void arrayhex(FILE *f,const double *x,int n){fputc('[',f);for(int i=0;i<n;i++){if(i)fputc(',',f);hx(f,x[i]);}fputc(']',f);}
static void closeok(FILE *f){if(ferror(f)){fclose(f);exit(96);}if(fclose(f))exit(96);}
static void trialset(struct thermodynamics_parameters_and_workspace *a,int trial){
 struct thermo_reionization_parameters *rp=a->ptw->ptrp;
 double center=trial?0.:a->ppr->reionization_z_start_max-a->ppr->reionization_start_factor*a->pth->reionization_width;
 double start=trial?fmax(a->ppr->reionization_start_factor*a->pth->reionization_width,a->pth->helium_fullreio_redshift+a->ppr->reionization_start_factor*a->pth->helium_fullreio_width):a->ppr->reionization_z_start_max;
 rp->reionization_parameters[rp->index_re_reio_redshift]=center;
 rp->reionization_parameters[rp->index_re_reio_start]=start;
}

int thermodynamics_reionization_evolve_with_tau(struct thermodynamics_parameters_and_workspace *a,double ini,double end,double *grid,int size){
 char err[_ERRORMSGSIZE_]="";q042_tau_entries++;
 if(q042_tau_entries!=1||sizeof(double)!=8||DBL_MANT_DIG!=53||FLT_RADIX!=2||fegetround()!=FE_TONEAREST||
    a->pth->reio_parametrization!=reio_camb||a->pth->reio_z_or_tau!=reio_tau||ini!=-50.||end!=0.||size!=28333||size!=a->pth->tt_size||q042_adapter_preflight(a,ini,err,sizeof err)){
  fprintf(stderr,"Q042_CONTEXT_PREFLIGHT=FAIL %s\n",err);exit(91);
 }
 struct background *ba=a->pba;struct thermo_workspace *w=a->ptw;
 struct thermo_diffeq_workspace *d=w->ptdw;struct thermo_vector *v=d->ptv;
 HYREC_DATA *hy=d->phyrec->data;HYREC_ATOMIC *at=hy->atomic;
 struct thermo_reionization_parameters *rp=w->ptrp;double *re=rp->reionization_parameters;
 /* Adapter probes mutate RHS scratch, including xe_before. Restore entry scratch
  * by a single original RHS evaluation before recording its context. */
 double entry_dy[3]={0};
 if(thermodynamics_derivs(ini,v->y,entry_dy,a,err)==_FAILURE_){fprintf(stderr,"Q042_ENTRY_SCRATCH_RESTORE=FAIL %s\n",err);exit(92);}
 if(v->y[0]!=-86.955287923490403||v->y[2]!=.00024187860481588748||v->y[1]!=1.2261504557092879e-5||w->fHe!=.081556058814182833||w->Tcmb!=2.7254999999999998||w->SIunit_nH0!=.17567299793393323||a->pth->tau_reio!=.022146719553358576){fputs("Q042_ARCHIVED_ENTRY_GATE=FAIL\n",stderr);exit(92);}
 if(ba->bt_size<2||ba->bt_size>200000||!at||!hy->fit||hy->error||hy->cosmo->fsR!=1.||hy->cosmo->meR!=1.||MODEL!=SWIFT||d->ap_current<1||d->ap_current!=d->index_ap_reio||d->require_H!=_TRUE_||d->require_He!=_FALSE_){fputs("Q042_CONTEXT_DOMAIN_GATE=FAIL\n",stderr);exit(93);}
 FILE *f=q042_open("initialized_context.json","w");if(!f)exit(94);
 q042_identity(f,"ORIGINAL_CONTEXT");
 fputs(",\"schema\":1,\"number_encoding\":\"C99_hex_exact_binary64\",\"tau_search_executed\":false,\"history_integrated\":false,\"flags\":{\"hyrec\":true,\"reio_camb\":true,\"no_exotic\":true,\"no_varconst\":true,\"no_idm\":true,\"no_idr\":true,\"no_idm_b\":true,\"require_H\":true,\"require_He\":false,\"phase_reio\":true,\"MODEL_SWIFT\":true,\"hyrec_error_zero\":true,\"fsR_meR_one\":true},\"constants\":{",f);
 kv(f,"Tcmb",w->Tcmb,0);kv(f,"nH0",w->SIunit_nH0,1);kv(f,"fHe",w->fHe,1);kv(f,"helium",v->y[1],1);kv(f,"helium_cutoff",d->phyrec->xHeII_limit,1);
 kv(f,"c",_c_,1);kv(f,"Mpc",_Mpc_over_m_,1);kv(f,"sigma",_sigma_,1);kv(f,"me",_m_e_,1);kv(f,"Jm3",_Jm3_over_Mpc2_,1);kv(f,"cm3",1e-6,1);
 kv(f,"kBoltz",kBoltz,1);kv(f,"TR_MIN",TR_MIN,1);kv(f,"TR_MAX",TR_MAX,1);kv(f,"T_RATIO_MIN",T_RATIO_MIN,1);
 kv(f,"SAHA",SAHA_FACT(1.,1.),1);kv(f,"LYA",LYA_FACT(1.,1.),1);kv(f,"EI",EI,1);kv(f,"L2s",L2s1s,1);
 kv(f,"alpha_pref",4.309e-13,1);kv(f,"alpha_pow1",-.6166,1);kv(f,"alpha_den",.6703,1);kv(f,"alpha_pow2",.5300,1);
 fputs("},\"accepted_D_He_H\":",f);arrayhex(f,v->y,3);
 fprintf(f,",\"grid_size\":%d,\"bg_size\":%d,\"bg_H_index\":%d,\"bg_rhog_index\":%d,\"background_columns\":[\"loga\",\"H_Mpc-1\",\"rho_g_Mpc-2\",\"d2H_dloga2\",\"d2rho_g_dloga2\"],\"background\":[",size,ba->bg_size,ba->index_bg_H,ba->index_bg_rho_g);
 for(int i=0;i<ba->bt_size;i++){
  if(i){fputc(',',f);}
  double row[5]={ba->loga_table[i],ba->background_table[i*ba->bg_size+ba->index_bg_H],ba->background_table[i*ba->bg_size+ba->index_bg_rho_g],ba->d2background_dloga2_table[i*ba->bg_size+ba->index_bg_H],ba->d2background_dloga2_table[i*ba->bg_size+ba->index_bg_rho_g]};arrayhex(f,row,5);
 }
 fputs("],\"logAlpha\":[",f);
 for(int l=0;l<4;l++){if(l)fputc(',',f);fputc('[',f);for(int m=0;m<NTM;m++){if(m)fputc(',',f);arrayhex(f,at->logAlpha_tab[l][m],NTR);}fputc(']',f);}fputs("],\"logR\":",f);arrayhex(f,at->logR2p2s_tab,NTR);
 fputs(",\"logTR_grid\":",f);arrayhex(f,at->logTR_tab,NTR);fputs(",\"T_RATIO_grid\":",f);arrayhex(f,at->T_RATIO_tab,NTM);
 fputs(",\"DlogTR\":",f);hx(f,at->DlogTR);fputs(",\"DT_RATIO\":",f);hx(f,at->DT_RATIO);fputs(",\"fit_first_K\":",f);hx(f,hy->fit->swift_func[0][0]);
 fprintf(f,",\"phase\":{\"current\":%d,\"previous\":%d,\"reio\":%d,\"full_recombination\":%d,\"previous_limit\":",d->ap_current,d->ap_current-1,d->index_ap_reio,d->index_ap_frec);hx(f,d->ap_z_limits[d->ap_current-1]);fputs(",\"smoothing_delta\":",f);hx(f,d->ap_z_limits_delta[d->ap_current]);fputs("},\"entry_reionization_parameters\":",f);arrayhex(f,re,rp->re_size);
 fputs(",\"trials\":{",f);
 for(int t=0;t<2;t++){
  trialset(a,t);if(t)fputc(',',f);q042_string(f,t?"LOWER":"UPPER");fputs(":{",f);
  kv(f,"center",re[rp->index_re_reio_redshift],0);kv(f,"start",re[rp->index_re_reio_start],1);kv(f,"exponent",re[rp->index_re_reio_exponent],1);kv(f,"width",re[rp->index_re_reio_width],1);kv(f,"after",re[rp->index_re_xe_after],1);kv(f,"he_fraction",re[rp->index_re_helium_fullreio_fraction],1);kv(f,"he_center",re[rp->index_re_helium_fullreio_redshift],1);kv(f,"he_width",re[rp->index_re_helium_fullreio_width],1);fputc('}',f);
 }
 fputs("}}\n",f);closeok(f);
 f=q042_open("native_grid_hex.json","w");if(!f)exit(94);q042_identity(f,"GRID");fputs(",\"columns\":[\"z_by_row\",\"eta_Mpc_by_row\",\"mz_by_output_index\"],\"rows\":[",f);
 for(int i=0;i<size;i++){if(i)fputc(',',f);double row[3]={a->pth->z_table[i],a->pth->tau_table[i],grid[i]};arrayhex(f,row,3);}fputs("]}\n",f);closeok(f);
 for(int i=0;i<size;i++)a->pth->thermodynamics_table[i*a->pth->th_size+a->pth->index_th_dddkappa]=NAN;
 if(q042_export_table(a,"SHARED_PREFIX",err,sizeof err)){fprintf(stderr,"%s\n",err);exit(94);}
 /* Finite independent boxes, NOT successive steps or history values. */
 const double zs[12]={50.,40.,30.,30.,30.,20.,16.031010835587164,10.,7.5,3.5,0.,49.999};
 const double ratios[12]={0.,.375,.0999,.1001,1.,1.01,.2,.2,.2,.2,.2,.375};
 f=q042_open("original_rhs_points.jsonl","w");if(!f)exit(94);
 for(int t=0;t<2;t++){
  trialset(a,t);
  q042_physical_context ctx={0};ctx.a=a;ctx.helium=v->y[1];ctx.wrapper_fHe=hy->cosmo->fHe;ctx.deadline=q042_now()+30.;ctx.call_cap=12;ctx.branch=t?"LOWER":"UPPER";q042_active=&ctx;
  for(int j=0;j<12;j++){
   double yy[3]={j==0?v->y[0]:(ratios[j]-1.)*w->Tcmb*(1.+zs[j]),v->y[1],v->y[2]},dy[3]={0};
   int status=thermodynamics_derivs(-zs[j],yy,dy,a,err);
   q042_identity(f,ctx.branch);fprintf(f,",\"point\":%d,\"z\":",j);hx(f,zs[j]);fputs(",\"D_He_H\":",f);arrayhex(f,yy,3);fprintf(f,",\"original_status\":%d,\"dy_D_He_H\":[",status);
   for(int q=0;q<3;q++){if(q)fputc(',',f);q042_number(f,dy[q]);}fputs("],\"error\":",f);q042_string(f,status?err:"");fputs("}\n",f);fflush(f);
   if(status){closeok(f);fprintf(stderr,"Q042_ORIGINAL_POINT_GATE=FAIL %s\n",err);exit(97);}
  }
  q042_active=NULL;
 }
 closeok(f);puts("Q042_CONTEXT_CAPTURE=COMPLETE; NO_HISTORY_NO_TAU_SEARCH_NO_INFERENCE");fflush(NULL);exit(0);
}

int main(int argc,char **argv){
 struct precision pr;struct background ba;struct thermodynamics th;struct perturbations pt;struct primordial pm;struct fourier fo;struct transfer tr;struct harmonic hr;struct lensing le;struct distortions sd;struct output op;ErrorMsg err;
 q042_started=q042_now();q042_dir=getenv("Q042_CONTEXT_DIR");q042_run=getenv("Q042_CONTEXT_RUN");q042_config=getenv("Q042_CONTEXT_CONFIG_SHA256");
 if(argc!=2||!q042_dir||!q042_run||!q042_config||strlen(q042_config)!=64){fprintf(stderr,"Q042_NATIVE_ARGUMENT_GATE=FAIL\n");return 2;}
 if(input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err)==_FAILURE_){fprintf(stderr,"Q042_INPUT_GATE=FAIL %s\n",err);return 3;}
 if(background_init(&pr,&ba)==_FAILURE_){fprintf(stderr,"Q042_BACKGROUND_GATE=FAIL %s\n",ba.error_message);return 4;}
 /* Unchanged prefix runs until the exported tau-entry boundary. No spectra. */
 if(thermodynamics_init(&pr,&ba,&th)==_FAILURE_){fprintf(stderr,"Q042_PREFIX_OR_PREFLIGHT_GATE=FAIL %s\n",th.error_message);return 5;}
 fprintf(stderr,"Q042_TAU_ENTRY_INTERPOSITION_GATE=FAIL no expected exit\n");return 6;
}
