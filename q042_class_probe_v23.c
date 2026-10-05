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
  if (input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err)==_FAILURE_) {
    fprintf(stderr,"INPUT_GATE=FAIL %s\n",err);return 3;
  }
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
  free(v);fclose(meta);fclose(nodes);fclose(probe);fclose(extrema);
  if (thermodynamics_free(&th)==_FAILURE_ || background_free(&ba)==_FAILURE_) return 10;
  puts("Q042_NATIVE_THERMODYNAMIC_ATTRIBUTION=COMPLETE");return 0;
}
