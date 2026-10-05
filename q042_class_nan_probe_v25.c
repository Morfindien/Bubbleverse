/* Q-042: read-only access to the frozen thermodynamic table and interpolator.
 * Link against the verified original classy shared object for the HPC result.
 * No precision, table, interpolation or exception-policy changes are made.
 */
#include "class.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static FILE *open_output(const char *dir,const char *name) {
  char path[4096];
  if (snprintf(path,sizeof(path),"%s/%s",dir,name)>=(int)sizeof(path)) return NULL;
  return fopen(path,"w");
}

static int evaluate(struct background *ba,struct thermodynamics *th,double z,double *v,int *idx) {
  /* This diagnostic only queries inside the thermodynamic table. The source
   * ignores pvecback here, so no background interpolation is substituted. */
  if (z<0 || z>=th->z_table[th->tt_size-1]) return _FAILURE_;
  return thermodynamics_at_z(ba,th,z,inter_normal,idx,NULL,v);
}

static int is_linear(struct thermodynamics *th,double z) {
  return ((th->reio_parametrization==reio_half_tanh && z<2*th->z_reio)
       || (th->reio_parametrization==reio_inter && z<50));
}

/* Read-only exported-function observers. The original CLASS functions run
 * exactly once with the same arguments. No solver/source patch is applied. */
#include <dlfcn.h>
static FILE *trace_file;
static unsigned trace_events,tau_calls,get_tau_calls,source_calls;
static int trace_overflow,tau_active;
static void number(double x) {
  if (isnan(x)) fputs("\"NaN\"",trace_file);
  else if (isinf(x)) fputs(x>0?"\"Infinity\"":"\"-Infinity\"",trace_file);
  else fprintf(trace_file,"%.17g",x);
}
static int event(void) {
  if (trace_events>=256) {trace_overflow=1;return 0;}
  trace_events++;return 1;
}
static void *original(const char *name) {
  void *p=dlsym(RTLD_NEXT,name);
  if (!p) {fprintf(stderr,"ORIGINAL_SYMBOL_GATE=FAIL %s: %s\n",name,dlerror());exit(90);}
  return p;
}
#include "q042_class_nan_observers_v25.h"

int thermodynamics_reionization_get_tau(struct precision *pr,struct background *ba,
                                        struct thermodynamics *th,struct thermo_workspace *w) {
  typedef int (*fn)(struct precision*,struct background*,struct thermodynamics*,struct thermo_workspace*);
  static fn call;
  if (!call) call=(fn)original("thermodynamics_reionization_get_tau");
  int status=call(pr,ba,th,w);get_tau_calls++;
  if (event()) {
    fprintf(trace_file,"{\"event\":\"get_tau\",\"call\":%u,\"status\":%d,\"computed_tau\":",get_tau_calls,status);number(w->reionization_optical_depth);
    fputs(",\"reio_redshift\":",trace_file);number(w->ptrp->reionization_parameters[w->ptrp->index_re_reio_redshift]);
    fputs(",\"reio_start\":",trace_file);number(w->ptrp->reionization_parameters[w->ptrp->index_re_reio_start]);
    fputs(",\"first_conformal_times\":[",trace_file);
    for(int i=0;i<4;i++){if(i)fputc(',',trace_file);number(th->tau_table[i]);}
    fputs("],\"first_xe\":[",trace_file);
    for(int i=0;i<4;i++){if(i)fputc(',',trace_file);number(th->thermodynamics_table[i*th->th_size+th->index_th_xe]);}
    fputs("],\"first_dkappa\":[",trace_file);
    for(int i=0;i<4;i++){if(i)fputc(',',trace_file);number(th->thermodynamics_table[i*th->th_size+th->index_th_dkappa]);}
    fputs("],\"first_d3kappa\":[",trace_file);
    for(int i=0;i<4;i++){if(i)fputc(',',trace_file);number(th->thermodynamics_table[i*th->th_size+th->index_th_dddkappa]);}
    fputs("]}\n",trace_file);
  }
  return status;
}
int thermodynamics_sources(double mz,double *y,double *dy,int index_z,void *workspace,ErrorMsg err) {
  typedef int (*fn)(double,double*,double*,int,void*,ErrorMsg);
  static fn call;
  if (!call)call=(fn)original("thermodynamics_sources");
  int status=call(mz,y,dy,index_z,workspace,err);source_calls++;
  struct thermodynamics_parameters_and_workspace *a=workspace;
  int row=a->pth->tt_size-index_z-1;
  if(tau_active && row>=0 && row<5 && event()) {
    fprintf(trace_file,"{\"event\":\"source_row\",\"trial\":%u,\"status\":%d,\"row\":%d,\"ap_current\":%d,\"index_ap_reio\":%d,\"z\":",get_tau_calls+1,status,row,a->ptw->ptdw->ap_current,a->ptw->ptdw->index_ap_reio);number(-mz);
    fputs(",\"xe\":",trace_file);number(a->pth->thermodynamics_table[row*a->pth->th_size+a->pth->index_th_xe]);
    fputs(",\"x_noreio\":",trace_file);number(a->ptw->ptdw->x_noreio);
    fputs(",\"reio_start\":",trace_file);number(a->ptw->ptrp->reionization_parameters[a->ptw->ptrp->index_re_reio_start]);
    fputs("}\n",trace_file);
  }
  return status;
}
int thermodynamics_reionization_evolve_with_tau(struct thermodynamics_parameters_and_workspace *a,
                                                double ini,double end,double *out,int size) {
  typedef int (*fn)(struct thermodynamics_parameters_and_workspace*,double,double,double*,int);
  static fn call;
  if(!call)call=(fn)original("thermodynamics_reionization_evolve_with_tau");
  tau_calls++;tau_active=1;
  if(event()) {
    fputs("{\"event\":\"tau_enter\",\"requested_tau\":",trace_file);number(a->pth->tau_reio);
    fputs(",\"optical_depth_tolerance\":",trace_file);number(a->ppr->reionization_optical_depth_tol);
    fputs(",\"mz_ini\":",trace_file);number(ini);fputs(",\"mz_end\":",trace_file);number(end);fputs("}\n",trace_file);
  }
  int status=call(a,ini,end,out,size);tau_active=0;
  if(event()) {
    fprintf(trace_file,"{\"event\":\"tau_exit\",\"status\":%d,\"fitted_z_reio\":",status);number(a->pth->z_reio);
    fputs(",\"last_computed_tau\":",trace_file);number(a->ptw->reionization_optical_depth);fputs("}\n",trace_file);
  }
  return status;
}

int main(int argc,char **argv) {
  struct precision pr;
  struct background ba;
  struct thermodynamics th;
  struct perturbations pt;
  struct primordial pm;
  struct fourier fo;
  struct transfer tr;
  struct harmonic hr;
  struct lensing le;
  struct distortions sd;
  struct output op;
  ErrorMsg err;
  FILE *meta,*nodes,*probe,*extrema;
  double *v,z=0.05663014;
  int i,j,idx=0;
  const char *dir=getenv("Q042_TRACE_DIR");
  if (argc!=2 || dir==NULL) {fprintf(stderr,"Usage: Q042_TRACE_DIR=... probe point.ini\n");return 2;}
  trace_file=open_output(dir,"native_trace.jsonl");if(!trace_file)return 10;
  if (input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err)==_FAILURE_) {
    fprintf(stderr,"INPUT_GATE=FAIL %s\n",err);return 3;
  }
  fputs("{\"event\":\"input\",\"reio_z_or_tau\":",trace_file);fprintf(trace_file,"%d",(int)th.reio_z_or_tau);fputs(",\"tau_reio\":",trace_file);number(th.tau_reio);fputs(",\"initial_z_reio\":",trace_file);number(th.z_reio);fputs("}\n",trace_file);trace_events++;
  if (background_init(&pr,&ba)==_FAILURE_) {fprintf(stderr,"BACKGROUND_GATE=FAIL %s\n",ba.error_message);return 4;}
  if (thermodynamics_init(&pr,&ba,&th)==_FAILURE_) {fprintf(stderr,"THERMODYNAMICS_GATE=FAIL %s\n",th.error_message);return 5;}
  meta=open_output(dir,"native_meta.json");nodes=open_output(dir,"native_nodes.csv");
  probe=open_output(dir,"native_probe.json");extrema=open_output(dir,"native_extrema.csv");
  if (!meta || !nodes || !probe || !extrema) {fprintf(stderr,"OUTPUT_GATE=FAIL\n");return 6;}
  fprintf(meta,"{\"schema\":1,\"reionization_sampling\":%.17g,\"reionization_z_start_max\":%.17g,\"reio_parametrization_enum\":%d,\"z_reio\":%.17g,\"tt_size\":%d,\"th_size\":%d,\"active_spacing_override\":false,\"precision_changed\":false}\n",pr.reionization_sampling,pr.reionization_z_start_max,(int)th.reio_parametrization,th.z_reio,th.tt_size,th.th_size);
  fprintf(nodes,"z,xe,dkappa,d2xe_dz2,d2dkappa_dz2\n");
  for (i=0;i<th.tt_size;i++) {
    const int offset=i*th.th_size;
    fprintf(nodes,"%.17g,%.17g,%.17g,%.17g,%.17g\n",th.z_table[i],th.thermodynamics_table[offset+th.index_th_xe],th.thermodynamics_table[offset+th.index_th_dkappa],th.d2thermodynamics_dz2_table[offset+th.index_th_xe],th.d2thermodynamics_dz2_table[offset+th.index_th_dkappa]);
  }
  v=calloc((size_t)th.th_size,sizeof(double));if (v==NULL) return 7;
  if (evaluate(&ba,&th,z,v,&idx)==_FAILURE_) {fprintf(stderr,"INTERPOLATION_GATE=FAIL %s\n",th.error_message);return 8;}
  fprintf(probe,"{\"z\":%.17g,\"reported_z_is_rounded\":true,\"last_index\":%d,\"method\":\"%s\",\"xe\":%.17g,\"dkappa\":%.17g,\"tau_c\":%.17g}\n",z,idx,is_linear(&th,z)?"linear":"spline",v[th.index_th_xe],v[th.index_th_dkappa],1./v[th.index_th_dkappa]);
  /* Inspect only the finite redshift range containing reionization. Each
   * candidate is an analytic stationary point of a table interval, not a
   * parameter sweep. Values are evaluated by the original CLASS routine. */
  fprintf(extrema,"interval,column,z,xe,dkappa\n");
  for (i=0;i<th.tt_size-1 && th.z_table[i]<pr.reionization_z_start_max;i++) {
    double x0=th.z_table[i],h=th.z_table[i+1]-x0;
    if (h<=0 || is_linear(&th,x0+h/2)) continue;
    for (j=0;j<2;j++) {
      int col=j?th.index_th_dkappa:th.index_th_xe;
      double y0=th.thermodynamics_table[i*th.th_size+col],y1=th.thermodynamics_table[(i+1)*th.th_size+col];
      double d0=th.d2thermodynamics_dz2_table[i*th.th_size+col],d1=th.d2thermodynamics_dz2_table[(i+1)*th.th_size+col];
      double A=h*h*(d1-d0)/2,B=h*h*d0,C=y1-y0+h*h*(-2*d0-d1)/6;
      double roots[2];int n=0,k;
      if (A==0) {if (B!=0) roots[n++]=-C/B;}
      else {
        double disc=B*B-4*A*C;
        if (disc>=0) {
          double q=-0.5*(B+copysign(sqrt(disc),B));
          if (q==0) roots[n++]=-B/(2*A);
          else {roots[n++]=q/A;roots[n++]=C/q;}
        }
      }
      for (k=0;k<n;k++) if (roots[k]>0 && roots[k]<1) {
        double query=x0+h*roots[k];
        if (query>pr.reionization_z_start_max) continue;
        if (evaluate(&ba,&th,query,v,&idx)==_FAILURE_) return 9;
        fprintf(extrema,"%d,%s,%.17g,%.17g,%.17g\n",i,j?"dkappa":"xe",query,v[th.index_th_xe],v[th.index_th_dkappa]);
      }
    }
  }
  fprintf(trace_file,"{\"event\":\"final\",\"tau_calls\":%u,\"get_tau_calls\":%u,\"source_calls\":%u,\"trace_overflow\":%s,\"upstream_schema_error\":%s,\"upstream_calls\":{",tau_calls,get_tau_calls,source_calls,trace_overflow?"true":"false",upstream_schema_error?"true":"false");
  for(int k=0;k<5;k++){if(k)fputc(',',trace_file);fprintf(trace_file,"\"%s\":%u",upstream_names[k],upstream_calls[k]);}
  fputs("}}\n",trace_file);fclose(trace_file);
  free(v);fclose(meta);fclose(nodes);fclose(probe);fclose(extrema);
  if (thermodynamics_free(&th)==_FAILURE_ || background_free(&ba)==_FAILURE_) return 10;
  puts("Q042_NATIVE_THERMODYNAMIC_ATTRIBUTION=COMPLETE");return 0;
}
