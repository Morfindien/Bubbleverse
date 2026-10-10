/* Q045 observation only. Original functions execute once with original arguments.
 * Link -rdynamic to the pinned original classy SO, as in the repository V24 probe.
 * No original source/binary/table mutation. Input precision is deliberately refined.
 */
#include "class.h"
#include <dlfcn.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *directory;
static FILE *events,*species;
static unsigned calls,source_rows,cumulative_calls;
static int scalar_active,optical_active;
static struct thermodynamics *scalar_th,*optical_th;
static double nH0,fHe,YHe;

static FILE *output(const char *name) {
  char p[4096];
  if(!directory)directory=getenv("Q045_TRACE_DIR");
  if(!directory || snprintf(p,sizeof(p),"%s/%s",directory,name)>=(int)sizeof(p))exit(90);
  FILE *f=fopen(p,"w");if(!f)exit(91);return f;
}
static void init(void) {
  if(events)return;
  events=output("native_trace.jsonl");species=output("source_species.tsv");
  fputs("trial\trow\tz\tap\tx_H_workspace\tx_He_workspace\tx_noreio\tx_reio\txe_stored\tH_1_Mpc\n",species);
}
static void num(FILE *f,double x) {
  if(isnan(x))fputs("\"NaN\"",f);
  else if(isinf(x))fputs(x>0?"\"Infinity\"":"\"-Infinity\"",f);
  else fprintf(f,"%.17g",x);
}
static void *original(const char *name) {
  void *p=dlsym(RTLD_NEXT,name);
  if(!p){fprintf(stderr,"ORIGINAL_SYMBOL_GATE %s: %s\n",name,dlerror());exit(92);}return p;
}
static void dump_integral(const char *name,double *x,int n,double *a,int stride,int y,int d,int k,struct thermodynamics *th) {
  if(n<3 || n>200000 || stride<1 || x!=th->tau_table || a!=th->thermodynamics_table)exit(93);
  FILE *f=output(name);fputs("row\tz\teta_Mpc\tq_1_Mpc\tq_second_eta",f);
  fputs(k<0?"\n":"\tnative_kappa\n",f);
  for(int i=0;i<n;i++){
    fprintf(f,"%d\t%.17g\t%.17g\t%.17g\t%.17g",i,th->z_table[i],x[i],a[i*stride+y],a[i*stride+d]);
    if(k>=0)fprintf(f,"\t%.17g",-a[i*stride+k]);
    fputc('\n',f);
  }
  if(fclose(f))exit(94);
}

int array_integrate_all_spline_table_line_to_line(double *x,int n,double *a,int stride,int y,int d,double *r,ErrorMsg err) {
  typedef int(*fn)(double*,int,double*,int,int,int,double*,ErrorMsg);
  static fn call;if(!call)call=(fn)original("array_integrate_all_spline_table_line_to_line");
  int status=call(x,n,a,stride,y,d,r,err);
  if(scalar_active && status==_SUCCESS_) {
    if(y!=scalar_th->index_th_dkappa || d!=scalar_th->index_th_dddkappa)exit(95);
    char name[128];snprintf(name,sizeof(name),"scalar_%03u.tsv",calls+1);
    dump_integral(name,x,n,a,stride,y,d,-1,scalar_th);
  }
  return status;
}
int array_integrate_spline_table_line_to_line(double *x,int n,double *a,int stride,int y,int d,int k,ErrorMsg err) {
  typedef int(*fn)(double*,int,double*,int,int,int,int,ErrorMsg);
  static fn call;if(!call)call=(fn)original("array_integrate_spline_table_line_to_line");
  int status=call(x,n,a,stride,y,d,k,err);
  if(optical_active && y==optical_th->index_th_dkappa && d==optical_th->index_th_dddkappa && k==optical_th->index_th_g && status==_SUCCESS_) {
    cumulative_calls++;if(cumulative_calls!=1)exit(96);
    dump_integral("cumulative_native.tsv",x,n,a,stride,y,d,k,optical_th);
  }
  return status;
}
int thermodynamics_reionization_get_tau(struct precision *pr,struct background *ba,struct thermodynamics *th,struct thermo_workspace *w) {
  typedef int(*fn)(struct precision*,struct background*,struct thermodynamics*,struct thermo_workspace*);
  static fn call;if(!call)call=(fn)original("thermodynamics_reionization_get_tau");
  init();if(calls>=256)exit(97);scalar_active=1;scalar_th=th;
  int status=call(pr,ba,th,w);scalar_active=0;calls++;
  int j=0;double minimum=_HUGE_;
  for(int i=0;i<th->tt_size-1;i++)if(th->thermodynamics_table[i*th->th_size+th->index_th_xe]<minimum){minimum=th->thermodynamics_table[i*th->th_size+th->index_th_xe];j=i;}
  int n=j==0?0:(j<3?3:j);
  fprintf(events,"{\"event\":\"scalar\",\"call\":%u,\"status\":%d,\"argmin\":%d,\"support_rows\":%d,\"tau\":",calls,status,j,n);num(events,w->reionization_optical_depth);
  fputs(",\"z_reio\":",events);num(events,w->ptrp->reionization_parameters[w->ptrp->index_re_reio_redshift]);
  fputs(",\"reio_start\":",events);num(events,w->ptrp->reionization_parameters[w->ptrp->index_re_reio_start]);
  fputs(",\"endpoint_z\":",events);num(events,n?th->z_table[n-1]:0);fputs("}\n",events);fflush(events);return status;
}
int thermodynamics_calculate_opticals(struct precision *pr,struct thermodynamics *th) {
  typedef int(*fn)(struct precision*,struct thermodynamics*);
  static fn call;if(!call)call=(fn)original("thermodynamics_calculate_opticals");
  optical_active=1;optical_th=th;int status=call(pr,th);optical_active=0;return status;
}
int thermodynamics_sources(double mz,double *y,double *dy,int index_z,void *workspace,ErrorMsg err) {
  typedef int(*fn)(double,double*,double*,int,void*,ErrorMsg);
  static fn call;if(!call)call=(fn)original("thermodynamics_sources");
  int status=call(mz,y,dy,index_z,workspace,err);init();source_rows++;if(source_rows>1000000)exit(98);
  struct thermodynamics_parameters_and_workspace *a=workspace;
  struct thermo_diffeq_workspace *d=a->ptw->ptdw;int row=a->pth->tt_size-index_z-1;
  if(row<0 || row>=a->pth->tt_size)exit(99);
  /* Read the workspace after source returns. Smoothing can leave these fields
   * at the previous-regime evaluation; keep the stored blended total separately.
   * These are not independent post-reionization H/He species histories. */
  fprintf(species,"%u\t%d\t%.17g\t%d\t%.17g\t%.17g\t",calls+1,row,-mz,d->ap_current,d->x_H,d->x_He);
  fprintf(species,"%.17g",d->x_noreio);
  fprintf(species,"\t%.17g\t%.17g\t%.17g\n",d->x_reio,a->pth->thermodynamics_table[row*a->pth->th_size+a->pth->index_th_xe],a->pvecback[a->pba->index_bg_H]);
  return status;
}
int thermodynamics_reionization_evolve_with_tau(struct thermodynamics_parameters_and_workspace *a,double ini,double end,double *out,int n) {
  typedef int(*fn)(struct thermodynamics_parameters_and_workspace*,double,double,double*,int);
  static fn call;if(!call)call=(fn)original("thermodynamics_reionization_evolve_with_tau");init();
  nH0=a->ptw->SIunit_nH0;fHe=a->ptw->fHe;YHe=a->ptw->YHe;
  fputs("{\"event\":\"tau_enter\",\"requested_tau\":",events);num(events,a->pth->tau_reio);
  fputs(",\"relative_tolerance\":",events);num(events,a->ppr->reionization_optical_depth_tol);fputs("}\n",events);fflush(events);
  int status=call(a,ini,end,out,n);
  fprintf(events,"{\"event\":\"tau_exit\",\"status\":%d,\"tau\":",status);num(events,a->ptw->reionization_optical_depth);
  fputs(",\"z_reio\":",events);num(events,a->pth->z_reio);fputs("}\n",events);fflush(events);return status;
}

int main(int argc,char **argv) {
  struct precision pr;struct background ba;struct thermodynamics th;
  struct perturbations pt;struct primordial pm;struct fourier fo;struct transfer tr;
  struct harmonic hr;struct lensing le;struct distortions sd;struct output op;ErrorMsg err;
  if(argc!=2 || !getenv("Q045_TRACE_DIR"))return 2;
  init();
  if(input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err)==_FAILURE_){fprintf(stderr,"INPUT_GATE %s\n",err);return 3;}
  if(th.reio_parametrization!=reio_camb || th.reio_z_or_tau!=reio_tau){fputs("FROZEN_REIONIZATION_INPUT_GATE\n",stderr);return 12;}
  FILE *prec=output("effective_precision.tsv");
  #define class_precision_parameter(NAME,TYPE,DEF) fprintf(prec,#NAME "\t%.17g\n",(double)pr.NAME);
  #define class_type_parameter(NAME,READ,REAL,DEF) fprintf(prec,#NAME "\t%d\n",(int)pr.NAME);
  #define class_string_parameter(NAME,DIR,STRING) fprintf(prec,#NAME "\t%s\n",pr.NAME);
  #include "precisions.h"
  fclose(prec);
  if(background_init(&pr,&ba)==_FAILURE_){fprintf(stderr,"BACKGROUND_GATE %s\n",ba.error_message);return 4;}
  if(thermodynamics_init(&pr,&ba,&th)==_FAILURE_){fprintf(stderr,"THERMODYNAMICS_GATE %s\n",th.error_message);return 5;}
  FILE *nodes=output("final_native_nodes.tsv");
  fputs("row\tz\teta_Mpc\txe\tq_1_Mpc\texp_minus_kappa\tg_1_Mpc\td2xe_dz2\td2q_dz2\tH_1_Mpc\n",nodes);
  double *v=calloc((size_t)ba.bg_size,sizeof(double));int idx=0;if(!v)return 6;
  for(int i=0;i<th.tt_size;i++){
    if(background_at_z(&ba,th.z_table[i],long_info,inter_normal,&idx,v)==_FAILURE_)return 7;
    int o=i*th.th_size;
    fprintf(nodes,"%d\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\n",i,th.z_table[i],th.tau_table[i],th.thermodynamics_table[o+th.index_th_xe],th.thermodynamics_table[o+th.index_th_dkappa],th.thermodynamics_table[o+th.index_th_exp_m_kappa],th.thermodynamics_table[o+th.index_th_g],th.d2thermodynamics_dz2_table[o+th.index_th_xe],th.d2thermodynamics_dz2_table[o+th.index_th_dkappa],v[ba.index_bg_H]);
  }
  fclose(nodes);free(v);
  FILE *meta=output("native_meta.json");
  fprintf(meta,"{\"q\":\"Q-045\",\"treatment\":\"00\",\"precision_changed\":true,\"source_patch\":false,\"nH0_m3\":%.17g,\"fHe\":%.17g,\"YHe\":%.17g,\"sigma_m2\":%.17g,\"metres_per_Mpc\":%.17g,\"c_m_s\":%.17g,\"m_H_kg\":%.17g,\"not4\":%.17g,\"tau_reported\":%.17g,\"z_reio\":%.17g,\"rows\":%d,\"has_exotic_injection\":%d,\"has_varconst\":%d,\"has_idm_g\":%d,\"reio_parametrization\":%d}\n",nH0,fHe,YHe,_sigma_,_Mpc_over_m_,_c_,_m_H_,_not4_,th.tau_reio,th.z_reio,th.tt_size,th.has_exotic_injection,th.has_varconst,th.has_idm_g,(int)th.reio_parametrization);fclose(meta);
  fprintf(events,"{\"event\":\"final\",\"scalar_calls\":%u,\"cumulative_calls\":%u,\"source_rows\":%u}\n",calls,cumulative_calls,source_rows);
  if(fclose(events) || fclose(species))return 10;
  if(cumulative_calls!=1 || calls<2)return 8;
  if(thermodynamics_free(&th)==_FAILURE_ || background_free(&ba)==_FAILURE_)return 9;
  puts("OPTICAL_OBSERVATION_GATE=COMPLETE REFERENCE_GATE=UNQUALIFIED");return 0;
}
