"""Finite forwarding test of the actual frozen derivative body with controlled boundaries.
The boundary callbacks are fixtures. This is not a cosmological reference calculation.
"""
from pathlib import Path
import hashlib, subprocess, sys, tempfile

SOURCE_SHA='d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6'

FIXTURE=r'''
#define Q042_ADAPTER_FIXTURE
#include "q042_switch_native_v27.c"
#include <assert.h>
#include <stdarg.h>
void class_protect_sprintf(char*dest,char*tpl,...){va_list args;va_start(args,tpl);vsnprintf(dest,_ERRORMSGSIZE_,tpl,args);va_end(args);}
static int h_calls,he_calls;
static double expected_he=1.2261504557092879e-5;
int background_at_z(struct background*b,double z,enum vecback_format fmt,enum interpolation_method mode,int*last,double*v){v[b->index_bg_H]=1e-4;v[b->index_bg_rho_g]=1e-10;return _SUCCESS_;}
int thermodynamics_ionization_fractions(double z,double*y,struct background*b,struct thermodynamics*t,struct thermo_workspace*w,int ap){
 struct thermo_vector*v=w->ptdw->ptv;w->ptdw->x_H=y[v->index_ti_x_H];w->ptdw->x_He=y[v->index_ti_x_He];
 w->ptdw->x_noreio=w->ptdw->x_H+w->fHe*w->ptdw->x_He;w->ptdw->x_reio=.2+w->ptdw->x_noreio;return _SUCCESS_;
}
int hyrec_dx_H_dz(struct thermodynamics*t,struct thermohyrec*h,double xH,double xHe,double xe,double nH,double z,double H,double Tm,double Tr,double alpha,double me,double*out){
 h_calls++;assert(xHe==expected_he);assert(xe==xH+h->data->cosmo->fHe*xHe);assert(alpha==1&&me==1);*out=xe+.001*Tm;return _SUCCESS_;
}
int hyrec_dx_He_dz(struct thermodynamics*t,struct thermohyrec*h,double xH,double xHe,double xe,double nH,double z,double H,double Tm,double Tr,double alpha,double me,double*out){he_calls++;*out=0.;return _SUCCESS_;}
int recfast_dx_H_dz(struct thermodynamics*t,struct thermorecfast*r,double a,double b,double c,double d,double e,double f,double g,double*out){assert(0);return _FAILURE_;}
int recfast_dx_He_dz(struct thermodynamics*t,struct thermorecfast*r,double a,double b,double c,double d,double e,double f,double g,double h,double*out){assert(0);return _FAILURE_;}
int injection_calculate_at_z(struct background*b,struct thermodynamics*t,double x,double z,double T,double*v){assert(0);return _FAILURE_;}
int thermodynamics_idm_quantities(struct background*b,double z,double*y,double*dy,struct thermodynamics*t,struct thermo_workspace*w,double*v){assert(0);return _FAILURE_;}
#include "frozen_derivs_body.c"
int main(void){
 q042_dir=".";q042_run="FIXTURE";q042_config="FIXTURE";
 struct background ba={0};struct thermodynamics th={0};struct precision pr={0};struct thermo_workspace w={0};
 struct thermo_diffeq_workspace d={0};struct thermo_vector v={0};struct thermohyrec hy={0};HYREC_DATA data={0};REC_COSMOPARAMS cosmo={0};
 double back[3]={0},y[3]={-86.955287923490403,1.2261504557092879e-5,.00024187860481588748},original[3],reduced[3];ErrorMsg err;
 ba.index_bg_H=0;ba.index_bg_rho_g=1;pr.reionization_z_start_max=50;pr.z_end_reco_test=100;
 th.recombination=hyrec;w.ptdw=&d;w.Tcmb=2.7255;w.SIunit_nH0=.2;w.fHe=.081556058814182833;
 d.ptv=&v;d.phyrec=&hy;d.ap_current=d.index_ap_reio=7;d.index_ap_brec=0;
 v.ti_size=3;v.index_ti_D_Tmat=0;v.index_ti_x_He=1;v.index_ti_x_H=2;v.y=y;
 hy.data=&data;data.cosmo=&cosmo;cosmo.fHe=w.fHe;hy.xHeII_limit=1e-6;
 struct thermodynamics_parameters_and_workspace a={0};a.pba=&ba;a.pth=&th;a.ppr=&pr;a.ptw=&w;a.pvecback=back;
 q042_original_derivs=q042_frozen_derivs;
 assert(q042_eligible(&a,expected_he));assert(!q042_eligible(&a,1e-3));
 q042_physical_context c={0};c.a=&a;c.helium=expected_he;c.deadline=q042_now()+10;c.call_cap=100;
 for(int probe=0;probe<3;probe++){
  y[0]+=.1*probe;y[2]+=1e-7*probe;d.require_H=d.require_He=_TRUE_;
  assert(q042_frozen_derivs(-50,y,original,&a,err)==_SUCCESS_);int before=he_calls;
  d.require_He=_FALSE_;q042_active=&c;for(int j=0;j<3;j++)reduced[j]=NAN;
  assert(thermodynamics_derivs(-50,y,reduced,&a,err)==_SUCCESS_);
  assert(he_calls==before&&reduced[1]==0.&&original[0]==reduced[0]&&original[2]==reduced[2]);
  /* Explicit expected coupling checks catch a wrong temperature/H rate input. */
  assert(reduced[2]==-(d.x_noreio+.001*(y[0]+w.Tcmb*51.)));
  double Hz=back[0]*_c_/_Mpc_over_m_,rate=(2.*_sigma_/_m_e_/_c_)*(4./3.*back[1]*_Jm3_over_Mpc2_)*d.x_reio/(1.+d.x_reio+w.fHe);
  double expected=-(2.*(y[0]+w.Tcmb*51.)/51.+rate*y[0]/(Hz*51.)-w.Tcmb);
  assert(reduced[0]==expected);q042_active=NULL;
 }
 assert(h_calls==6&&he_calls==3&&c.calls==3);
 d.require_He=_FALSE_;q042_active=&c;double bad[3]={y[0],0.,y[2]};assert(thermodynamics_derivs(-50,bad,reduced,&a,err)==_FAILURE_);q042_active=NULL;
 puts("Q042_FROZEN_BODY_ADAPTER_FIXTURE=PASS controlled boundaries; no physical accuracy claim");return 0;
}
'''

def run(root):
    root=Path(root).resolve(); here=Path(__file__).resolve().parent
    source=root/'source/thermodynamics.c'
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_SHA: raise ValueError('FROZEN_DERIVATIVE_SOURCE_GATE=FAIL')
    text=source.read_text(); start=text.index('int thermodynamics_derivs('); end=text.index('\n/**\n * This function is relevant for the rk evolver',start)
    body=text[start:end].replace('int thermodynamics_derivs(','static int q042_frozen_derivs(',1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);(tmp/'frozen_derivs_body.c').write_text(body);(tmp/'fixture.c').write_text(FIXTURE)
        cmd=['gcc','-O2','-std=c99','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-Wno-unused-function','-Wno-unused-but-set-variable','-ffunction-sections','-fdata-sections','-fno-fast-math','-ffp-contract=off','-I'+str(here)]
        for d in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'): cmd+=['-I'+str(root/d)]
        cmd+=[str(tmp/'fixture.c'),'-Wl,--gc-sections','-ldl','-lm','-o',str(tmp/'fixture')]
        built=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        if built.returncode or built.stderr: raise AssertionError(built.stderr)
        tested=subprocess.run([str(tmp/'fixture')],capture_output=True,text=True,timeout=10)
        if tested.returncode: raise AssertionError(tested.stdout+tested.stderr)
        print(tested.stdout.strip())

if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'external/class_ede')
