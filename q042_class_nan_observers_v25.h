/* Q-042 V25: read-only exported-function boundary observations.
 * Original CLASS function is called once with identical arguments and return.
 * No scalar is replaced. First observed NaN is not claimed as global first NaN.
 */
#ifndef Q042_CLASS_NAN_OBSERVERS_V25
#define Q042_CLASS_NAN_OBSERVERS_V25
#define NAN_FIELDS 16
#define NAN_TRIALS 128
static const char *upstream_names[5]={"thermodynamics_derivs","thermodynamics_ionization_fractions","thermodynamics_reionization_function","hyrec_dx_H_dz","hyrec_dx_He_dz"};
static unsigned upstream_calls[5];
static int upstream_schema_error;
struct nan_sample {
  unsigned call;double z;int ni,no;
  const char *in_names[NAN_FIELDS],*out_names[NAN_FIELDS];
  double in[NAN_FIELDS],out[NAN_FIELDS];
};
struct nan_history {int initial,bad,have_previous;struct nan_sample previous;};
static struct nan_history upstream_history[NAN_TRIALS][5][2];
static int nan_all_finite(const double *v,int n){for(int i=0;i<n;i++)if(!isfinite(v[i]))return 0;return 1;}
static void nan_fields(const char *const *names,const double *v,int n){
  fputc('{',trace_file);
  for(int i=0;i<n;i++){if(i)fputc(',',trace_file);fprintf(trace_file,"\"%s\":",names[i]);number(v[i]);}
  fputc('}',trace_file);
}
static void nan_previous(const struct nan_sample *s){
  fprintf(trace_file,"{\"call\":%u,\"z\":",s->call);number(s->z);
  fputs(",\"inputs\":",trace_file);nan_fields(s->in_names,s->in,s->ni);
  fputs(",\"outputs\":",trace_file);nan_fields(s->out_names,s->out,s->no);fputc('}',trace_file);
}
static void nan_observe(int boundary,int phase,unsigned call,double z,
                        const char *const *in_names,const double *in,int ni,
                        const char *const *out_names,const double *out,int no,int status){
  unsigned trial=get_tau_calls+1;
  if(!tau_active)return;
  if(trial>=NAN_TRIALS || ni>NAN_FIELDS || no>NAN_FIELDS || !isfinite(z)){upstream_schema_error=1;return;}
  struct nan_history *h=&upstream_history[trial][boundary][phase];
  int fi=nan_all_finite(in,ni),fo=nan_all_finite(out,no),bad=!(fi&&fo);
  const char *kind=NULL;
  if(bad && !h->bad){h->bad=1;kind="first_nonfinite";}
  else if(!bad && !h->initial){h->initial=1;kind="initial";}
  if(kind && event()){
    fprintf(trace_file,"{\"event\":\"upstream\",\"boundary\":\"%s\",\"phase\":\"%s\",\"kind\":\"%s\",\"trial\":%u,\"call\":%u,\"z\":",upstream_names[boundary],phase?"exit":"entry",kind,trial,call);number(z);
    fprintf(trace_file,",\"status\":%d,\"inputs_finite\":%s,\"outputs_finite\":%s,\"inputs\":",status,fi?"true":"false",fo?"true":"false");nan_fields(in_names,in,ni);
    fputs(",\"outputs\":",trace_file);nan_fields(out_names,out,no);
    fputs(",\"previous_finite\":",trace_file);
    if(h->have_previous)nan_previous(&h->previous);else fputs("null",trace_file);
    fputs("}\n",trace_file);
  }
  if(!bad){
    h->have_previous=1;h->previous.call=call;h->previous.z=z;h->previous.ni=ni;h->previous.no=no;
    for(int i=0;i<ni;i++){h->previous.in_names[i]=in_names[i];h->previous.in[i]=in[i];}
    for(int i=0;i<no;i++){h->previous.out_names[i]=out_names[i];h->previous.out[i]=out[i];}
  }
}
static int nan_state_valid(struct thermo_workspace *w){
  struct thermo_vector *v=w->ptdw->ptv;
  int ok=v && v->ti_size==3 && v->index_ti_D_Tmat>=0 && v->index_ti_D_Tmat<v->ti_size && v->index_ti_x_H>=0 && v->index_ti_x_H<v->ti_size && v->index_ti_x_He>=0 && v->index_ti_x_He<v->ti_size && v->index_ti_D_Tmat!=v->index_ti_x_H && v->index_ti_D_Tmat!=v->index_ti_x_He && v->index_ti_x_H!=v->index_ti_x_He && w->ptdw->require_H && w->ptdw->require_He;
  if(!ok)upstream_schema_error=1;
  return ok;
}
int thermodynamics_derivs(double mz,double *y,double *dy,void *workspace,ErrorMsg err){
  typedef int(*fn)(double,double*,double*,void*,ErrorMsg);static fn call;
  if(!call)call=(fn)original("thermodynamics_derivs");
  struct thermodynamics_parameters_and_workspace *a=workspace;struct thermo_workspace *w=a->ptw;struct thermo_vector *v=w->ptdw->ptv;
  int active=tau_active && w->ptdw->ap_current==w->ptdw->index_ap_reio;
  unsigned count=active?++upstream_calls[0]:0;
  int valid=active && nan_state_valid(w);
  static const char *in_names[]={"z","D_Tmat","x_H","x_He","Tcmb","fHe","recombination","thermo_evolver"};
  static const char *out_names[]={"dD_Tmat","dx_H","dx_He","x_noreio","x_reio"};
  double in[8];
  if(valid){in[0]=-mz;in[1]=y[v->index_ti_D_Tmat];in[2]=y[v->index_ti_x_H];in[3]=y[v->index_ti_x_He];in[4]=w->Tcmb;in[5]=w->fHe;in[6]=a->pth->recombination;in[7]=a->ppr->thermo_evolver;nan_observe(0,0,count,-mz,in_names,in,8,NULL,NULL,0,0);}
  int status=call(mz,y,dy,workspace,err);
  if(valid){
    double out[5];int n=0;
    /* dy is inspected only after a successful original call in the three-state regime. */
    if(status==_SUCCESS_){out[0]=dy[v->index_ti_D_Tmat];out[1]=dy[v->index_ti_x_H];out[2]=dy[v->index_ti_x_He];out[3]=w->ptdw->x_noreio;out[4]=w->ptdw->x_reio;n=5;}
    nan_observe(0,1,count,-mz,in_names,in,8,out_names,out,n,status);
  }
  return status;
}
int thermodynamics_ionization_fractions(double z,double *y,struct background *ba,struct thermodynamics *th,struct thermo_workspace *w,int current_ap){
  typedef int(*fn)(double,double*,struct background*,struct thermodynamics*,struct thermo_workspace*,int);static fn call;
  if(!call)call=(fn)original("thermodynamics_ionization_fractions");
  int active=tau_active && current_ap==w->ptdw->index_ap_reio;unsigned count=active?++upstream_calls[1]:0;
  int valid=active && nan_state_valid(w);struct thermo_vector *v=w->ptdw->ptv;
  static const char *in_names[]={"z","D_Tmat","x_H","x_He","fHe"};
  static const char *out_names[]={"x_H","x_He","x_noreio","x_reio"};double in[5];
  if(valid){in[0]=z;in[1]=y[v->index_ti_D_Tmat];in[2]=y[v->index_ti_x_H];in[3]=y[v->index_ti_x_He];in[4]=w->fHe;nan_observe(1,0,count,z,in_names,in,5,NULL,NULL,0,0);}
  int status=call(z,y,ba,th,w,current_ap);
  if(valid){double out[4];int n=0;if(status==_SUCCESS_){out[0]=w->ptdw->x_H;out[1]=w->ptdw->x_He;out[2]=w->ptdw->x_noreio;out[3]=w->ptdw->x_reio;n=4;}nan_observe(1,1,count,z,in_names,in,5,out_names,out,n,status);}
  return status;
}
int thermodynamics_reionization_function(double z,struct thermodynamics *th,struct thermo_reionization_parameters *p,double *x){
  typedef int(*fn)(double,struct thermodynamics*,struct thermo_reionization_parameters*,double*);static fn call;
  if(!call)call=(fn)original("thermodynamics_reionization_function");
  int active=tau_active && th->reio_parametrization==reio_camb;unsigned count=active?++upstream_calls[2]:0;
  static const char *in_names[]={"z","xe_before","xe_after","center","start","width","exponent","helium_fraction","helium_redshift","helium_width"};
  static const char *out_names[]={"xe"};double in[10];
  if(active){
    int idx[]={p->index_re_xe_before,p->index_re_xe_after,p->index_re_reio_redshift,p->index_re_reio_start,p->index_re_reio_width,p->index_re_reio_exponent,p->index_re_helium_fullreio_fraction,p->index_re_helium_fullreio_redshift,p->index_re_helium_fullreio_width};
    for(int i=0;i<9;i++)if(idx[i]<0 || idx[i]>=p->re_size){upstream_schema_error=1;active=0;}
    if(active){in[0]=z;for(int i=0;i<9;i++)in[i+1]=p->reionization_parameters[idx[i]];nan_observe(2,0,count,z,in_names,in,10,NULL,NULL,0,0);}
  }
  int status=call(z,th,p,x);
  if(active)nan_observe(2,1,count,z,in_names,in,10,out_names,x,status==_SUCCESS_?1:0,status);
  return status;
}
#define NAN_HYREC_WRAPPER(NAME,B,OUTPUT_NAME) \
int NAME(struct thermodynamics *th,struct thermohyrec *hy,double xH,double xHe,double xe,double nH,double z,double Hz,double Tm,double Tr,double alpha,double me,double *out){ \
  typedef int(*fn)(struct thermodynamics*,struct thermohyrec*,double,double,double,double,double,double,double,double,double,double,double*);static fn call; \
  if(!call)call=(fn)original(#NAME); \
  unsigned count=tau_active?++upstream_calls[B]:0; \
  static const char *in_names[]={"x_H","x_He","xe","nH","z","Hz","Tmat","Trad","alpha","me"}; \
  static const char *out_names[]={OUTPUT_NAME};double in[]={xH,xHe,xe,nH,z,Hz,Tm,Tr,alpha,me}; \
  if(tau_active)nan_observe(B,0,count,z,in_names,in,10,NULL,NULL,0,0); \
  int status=call(th,hy,xH,xHe,xe,nH,z,Hz,Tm,Tr,alpha,me,out); \
  if(tau_active)nan_observe(B,1,count,z,in_names,in,10,out_names,out,status==_SUCCESS_?1:0,status); \
  return status; \
}
NAN_HYREC_WRAPPER(hyrec_dx_H_dz,3,"dx_H_dz")
NAN_HYREC_WRAPPER(hyrec_dx_He_dz,4,"dx_He_dz")
#undef NAN_HYREC_WRAPPER
#endif
