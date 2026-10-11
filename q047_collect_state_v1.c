/* Q047 collection adapter v1. Link to ORIGINAL classy.so; never build CLASS.
 * A NEW reconstruction, not recovery of a historical initialized instance.
 * Hooks call original functions once with unchanged arguments, then only read.
 * Binary interposition and observation neutrality require runtime validation.
 */
#define _GNU_SOURCE
#include "class.h"
#include "wrap_hyrec.h"
#include <dlfcn.h>
#include <fenv.h>
#include <stdint.h>
#include <unistd.h>

static const char *directory, *case_name;
static int stage; /* 0 input/shooting; 1 final background; 2 final thermal */
static unsigned initial_calls[3], thermal_calls;
static struct background *final_ba;

static void die(const char *why) { fprintf(stderr,"Q047_CAPTURE_FAIL %s\n",why); exit(90); }
static FILE *out(const char *name, const char *mode) {
  char p[4096];
  if(snprintf(p,sizeof p,"%s/%s",directory,name)>=(int)sizeof p) die("OUTPUT_PATH");
  FILE *f=fopen(p,mode); if(!f)die("OUTPUT_CREATE"); return f;
}
static void close_ok(FILE *f) { if(ferror(f))die("WRITE"); if(fclose(f))die("CLOSE"); }
static void str(FILE *f,const char *s) {
  fputc('"',f);
  for(;*s;s++){unsigned char c=(unsigned char)*s;
    if(c=='"'||c=='\\'){fputc('\\',f);fputc(c,f);}
    else if(c<32)fprintf(f,"\\u%04x",c); else fputc(c,f);}
  fputc('"',f);
}
static void hx(FILE *f,double x) { if(!isfinite(x))die("NONFINITE"); fprintf(f,"\"%a\"",x); }
static void kv(FILE *f,const char *k,double x,int comma) {
  if(comma){fputc(',',f);} str(f,k);fputc(':',f);hx(f,x);
}
static void vec(FILE *f,const double *x,int n) {
  if(n<0||n>200000||(n&&!x))die("VECTOR_SIZE");
  fputc('[',f);for(int i=0;i<n;i++){if(i)fputc(',',f);hx(f,x[i]);}fputc(']',f);
}
static void *original(const char *name) {
  dlerror();void *p=dlsym(RTLD_NEXT,name);if(!p)die(name);return p;
}
static void identity(FILE *f) {
  fputs("{\"schema\":\"Q047_CAPTURE_V1\",\"case\":",f);str(f,case_name);
  fputs(",\"origin\":\"NEW_RECONSTRUCTION\",\"number_encoding\":\"C99_hex_binary64\"",f);
}

int background_initial_conditions(struct precision *pr,struct background *ba,
                                 double *back,double *y,double *loga) {
  typedef int(*fn)(struct precision*,struct background*,double*,double*,double*);
  static fn call;if(!call)call=(fn)original("background_initial_conditions");
  int status=call(pr,ba,back,y,loga);initial_calls[stage]++;
  if(stage==1&&status==_SUCCESS_){
    if(ba!=final_ba||initial_calls[1]!=1)die("FINAL_INITIALIZATION_MULTIPLICITY");
    FILE *f=out("accepted_initial_hex.json","wx");identity(f);
    fputs(",\"callback\":\"background_initial_conditions:return_before_evolver\",\"fields\":{",f);
    kv(f,"loga_ini",*loga,0);kv(f,"a_ini_native",back[ba->index_bg_a],1);
    if(ba->has_scf){kv(f,"phi_ini",y[ba->index_bi_phi_scf],1);
      kv(f,"phi_prime_ini",y[ba->index_bi_phi_prime_scf],1);}
    fprintf(f,"},\"bi_size\":%d,\"bi_indices\":{\"time\":%d,\"tau\":%d,\"rs\":%d,\"D\":%d,\"D_prime\":%d",
      ba->bi_size,ba->index_bi_time,ba->index_bi_tau,ba->index_bi_rs,ba->index_bi_D,ba->index_bi_D_prime);
    if(ba->has_scf)fprintf(f,",\"phi\":%d,\"phi_prime\":%d",ba->index_bi_phi_scf,ba->index_bi_phi_prime_scf);
    fputs("},\"integration_vector\":",f);vec(f,y,ba->bi_size);fputs("}\n",f);close_ok(f);
  }
  return status;
}

int thermodynamics_vector_init(struct precision *pr,struct background *ba,
                               struct thermodynamics *th,double mz,struct thermo_workspace *w) {
  typedef int(*fn)(struct precision*,struct background*,struct thermodynamics*,double,struct thermo_workspace*);
  static fn call;if(!call)call=(fn)original("thermodynamics_vector_init");
  int status=call(pr,ba,th,mz,w);
  if(stage==2&&status==_SUCCESS_){
    if(ba!=final_ba||++thermal_calls>512)die("THERMAL_CALLBACK");
    struct thermo_diffeq_workspace *d=w->ptdw;struct thermo_vector *v=d->ptv;
    if(!v||!d->phyrec||!d->phyrec->data||!d->phyrec->data->cosmo)die("HYREC_CONTEXT");
    FILE *f=out("thermal_starts_hex.jsonl","a");identity(f);
    fprintf(f,",\"event\":%u,\"phase\":%d,\"phase_indices\":{\"brec\":%d,\"He1\":%d,\"He1f\":%d,\"He2\":%d,\"H\":%d,\"frec\":%d,\"reio\":%d},\"require_H\":%d,\"require_He\":%d,\"D_index\":%d",
      thermal_calls,d->ap_current,d->index_ap_brec,d->index_ap_He1,d->index_ap_He1f,d->index_ap_He2,
      d->index_ap_H,d->index_ap_frec,d->index_ap_reio,d->require_H,d->require_He,v->index_ti_D_Tmat);
    if(d->require_H)fprintf(f,",\"H_index\":%d",v->index_ti_x_H);
    if(d->require_He)fprintf(f,",\"He_index\":%d",v->index_ti_x_He);
    fputs(",\"mz\":",f);hx(f,mz);fputs(",\"y\":",f);vec(f,v->y,v->ti_size);
    fputs(",\"constants\":{",f);
    kv(f,"Tcmb",w->Tcmb,0);kv(f,"nH0_SI",w->SIunit_nH0,1);kv(f,"fHe_CLASS",w->fHe,1);
    kv(f,"YHe",w->YHe,1);kv(f,"fHe_HyRec",d->phyrec->data->cosmo->fHe,1);
    kv(f,"C_NR",w->const_NR_numberdens,1);kv(f,"I_H",w->const_Tion_H,1);
    kv(f,"I_HeI",w->const_Tion_HeI,1);kv(f,"I_HeII",w->const_Tion_HeII,1);
    kv(f,"native_xHeII_limit",d->phyrec->xHeII_limit,1);
    fprintf(f,"},\"HyRec_error\":%d,\"HyRec_MODEL\":%d,\"ap_limits\":",d->phyrec->data->error,MODEL);
    vec(f,d->ap_z_limits,d->ap_size);fputs(",\"ap_deltas\":",f);vec(f,d->ap_z_limits_delta,d->ap_size);
    fputs("}\n",f);close_ok(f);
  }
  return status;
}

static void effective(struct background *ba,struct thermodynamics *th) {
  FILE *f=out("effective_background_hex.json","wx");identity(f);fputs(",\"fields\":{",f);
  kv(f,"H0",ba->H0,0);
  #define B(F) kv(f,#F,ba->F,1)
  B(K);B(Omega0_b);B(Omega0_cdm);B(Omega0_g);B(Omega0_lambda);B(Omega0_ur);B(T_cmb);
  #undef B
  fputs("},\"flags\":{",f);
  fprintf(f,"\"has_scf\":%d",ba->has_scf);
  #define FLAG(F) fprintf(f,",\"" #F "\":%d",(int)ba->F)
  FLAG(has_lambda);FLAG(has_cdm);FLAG(has_ncdm);FLAG(has_ur);FLAG(has_idm);FLAG(has_idr);
  FLAG(has_dcdm);FLAG(has_dr);FLAG(has_fld);FLAG(has_curvature);
  #undef FLAG
  fprintf(f,"},\"N_ncdm\":%d,\"thermal_flags\":{\"has_varconst\":%d,\"has_exotic_injection\":%d,\"has_idm_b\":%d,\"has_idm_g\":%d,\"has_idm_dr\":%d,\"recombination\":%d},\"scalar\":",
    ba->N_ncdm,th->has_varconst,th->has_exotic_injection,th->has_idm_b,th->has_idm_g,th->has_idm_dr,th->recombination);
  if(ba->has_scf){
    fprintf(f,"{\"attractor_ic_scf\":%d,\"scf_tuning_index\":%d,\"fields\":{",ba->attractor_ic_scf,ba->scf_tuning_index);
    kv(f,"n_scf",ba->n_scf,0);kv(f,"CC_scf",ba->CC_scf,1);kv(f,"phi_ini_scf",ba->phi_ini_scf,1);
    kv(f,"phi_prime_ini_scf",ba->phi_prime_ini_scf,1);
    fputs("},\"scf_parameters\":",f);vec(f,ba->scf_parameters,ba->scf_parameters_size);fputc('}',f);
  }else fputs("null",f);
  fputs(",\"neutrinos\":[",f);
  for(int n=0;n<ba->N_ncdm;n++){
    if(ba->got_files[n])die("DISTRIBUTION_FILE_NOT_IMPLEMENTED_FOR_FROZEN_CASE");
    if(n){fputc(',',f);}fprintf(f,"{\"got_files\":%d,\"quadrature_strategy\":%d,\"fields\":{",ba->got_files[n],ba->ncdm_quadrature_strategy[n]);
    kv(f,"M_ncdm",ba->M_ncdm[n],0);kv(f,"T_ncdm",ba->T_ncdm[n],1);kv(f,"deg_ncdm",ba->deg_ncdm[n],1);
    kv(f,"ksi_ncdm",ba->ksi_ncdm[n],1);kv(f,"factor_ncdm",ba->factor_ncdm[n],1);
    fputs("},\"q_ncdm_bg\":",f);vec(f,ba->q_ncdm_bg[n],ba->q_size_ncdm_bg[n]);
    fputs(",\"w_ncdm_bg\":",f);vec(f,ba->w_ncdm_bg[n],ba->q_size_ncdm_bg[n]);fputc('}',f);
  }
  fputs("],\"z_reio\":",f);hx(f,th->z_reio);fputs(",\"tau_reio\":",f);hx(f,th->tau_reio);
  fprintf(f,",\"rounding_mode\":%d,\"FE_TONEAREST\":%d}\n",fegetround(),FE_TONEAREST);close_ok(f);
}

static void table(const char *name,char *titles,double *data,int rows,int columns) {
  FILE *f=out(name,"wx");size_t n=strlen(titles);while(n&&titles[n-1]=='\t')n--;
  fprintf(f,"# %.*s\n",(int)n,titles);
  for(int i=0;i<rows;i++){for(int j=0;j<columns;j++){
    double v=data[(size_t)i*columns+j];if(!isfinite(v))die("TABLE_NONFINITE");
    fprintf(f,j?"\t%.17g":"%.17g",v);}fputc('\n',f);}close_ok(f);
}

int main(int argc,char **argv) {
  struct precision pr;struct background ba;struct thermodynamics th;struct perturbations pt;
  struct primordial pm;struct fourier fo;struct transfer tr;struct harmonic hr;
  struct lensing le;struct distortions sd;struct output op;ErrorMsg err;
  directory=getenv("Q047_CAPTURE_DIR");case_name=getenv("Q047_CAPTURE_CASE");
  if(argc!=2||!directory||!case_name||sizeof(double)!=8||DBL_MANT_DIG!=53||FLT_RADIX!=2||fegetround()!=FE_TONEAREST)return 2;
  /* Creating this file now ensures callback appends cannot reuse old evidence. */
  close_ok(out("thermal_starts_hex.jsonl","wx"));final_ba=&ba;
  if(input_init(argc,argv,&pr,&ba,&th,&pt,&tr,&pm,&hr,&fo,&le,&sd,&op,err))die(err);
  if(ba.shooting_failed)die("SHOOTING_FAILED");
  FILE *f=out("effective_precision.json","wx");fputs("{",f);int comma=0;
  #define class_precision_parameter(NAME,TYPE,DEF) if(comma++)fputc(',',f);str(f,#NAME);fputc(':',f);hx(f,(double)pr.NAME);
  #define class_type_parameter(NAME,READ,REAL,DEF) if(comma++)fputc(',',f);str(f,#NAME);fprintf(f,":%d",(int)pr.NAME);
  #define class_string_parameter(NAME,DIR,STRING) if(comma++)fputc(',',f);str(f,#NAME);fputc(':',f);str(f,pr.NAME);
  #include "precisions.h"
  #undef class_precision_parameter
  #undef class_type_parameter
  #undef class_string_parameter
  fputs("}\n",f);close_ok(f);
  stage=1;if(background_init(&pr,&ba))die(ba.error_message);
  if(initial_calls[1]!=1)die("BACKGROUND_INTERPOSITION_MISSING");
  stage=2;if(thermodynamics_init(&pr,&ba,&th))die(th.error_message);
  if(!thermal_calls)die("THERMAL_INTERPOSITION_MISSING");
  effective(&ba,&th);
  char titles[_MAXTITLESTRINGLENGTH_]={0};
  if(background_output_titles(&ba,titles)){die("BACKGROUND_TITLES");}int c=get_number_of_titles(titles);
  double *data=calloc((size_t)ba.bt_size*c,sizeof(double));if(!data)die("ALLOC");
  if(background_output_data(&ba,c,data)){die("BACKGROUND_OUTPUT");}table("native_background.tsv",titles,data,ba.bt_size,c);free(data);
  memset(titles,0,sizeof titles);if(thermodynamics_output_titles(&ba,&th,titles))die("THERMAL_TITLES");c=get_number_of_titles(titles);
  data=calloc((size_t)th.tt_size*c,sizeof(double));if(!data)die("ALLOC");
  if(thermodynamics_output_data(&ba,&th,c,data)){die("THERMAL_OUTPUT");}table("native_thermodynamics.tsv",titles,data,th.tt_size,c);free(data);
  FILE *maps=fopen("/proc/self/maps","r");if(!maps)die("LOADED_MAPS");f=out("runtime_maps.txt","wx");char line[8192];
  while(fgets(line,sizeof line,maps)){fputs(line,f);}if(ferror(maps))die("MAPS_READ");fclose(maps);close_ok(f);
  f=out("observation_counters.json","wx");fprintf(f,"{\"input_shooting_initial_calls\":%u,\"final_initial_calls\":%u,\"thermal_start_calls\":%u,\"capture_completed\":true,\"historical_export\":false}\n",initial_calls[0],initial_calls[1],thermal_calls);close_ok(f);
  if(thermodynamics_free(&th)||background_free(&ba))die("FREE");
  puts("Q047_CAPTURE_COMPLETE RAW_RECONSTRUCTED_NOT_QUALIFIED");return 0;
}
