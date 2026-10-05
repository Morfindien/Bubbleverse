"""Q-042 finite diagnostic comparison with compiled pinned HyRec C routines.
Synthetic tables only: this does not claim the actual initialization was captured.
"""
import json,math,subprocess,sys,tempfile
from pathlib import Path
from q042_interval_v29 import Evaluator,I,jsonable

C_SOURCE=r'''
#include <stdio.h>
#include "history.h"
#include <stdlib.h>
int main(void){
 HYREC_ATOMIC a={0};REC_COSMOPARAMS c={0};INJ_PARAMS inj={0};HYREC_DATA d={0};char error[SIZE_ErrorM]={0};
 c.fsR=c.meR=1.;c.inj_params=&inj;d.atomic=&a;d.cosmo=&c;d.error_message=error;
 if(scanf("%lf%lf",&a.DlogTR,&a.DT_RATIO)!=2)return 2;
 for(int l=0;l<4;l++){a.logAlpha_tab[l]=malloc(NTM*sizeof(double*));for(int m=0;m<NTM;m++){a.logAlpha_tab[l][m]=malloc(NTR*sizeof(double));for(int n=0;n<NTR;n++)if(scanf("%lf",&a.logAlpha_tab[l][m][n])!=1)return 3;}}
 for(int n=0;n<NTR;n++)if(scanf("%lf",&a.logR2p2s_tab[n])!=1)return 4;
 double tr,ratio;
 while(scanf("%lf%lf",&tr,&ratio)==2){
  double aa[2],da[2],bb[2],r;
  interpolate_rates(aa,da,bb,&r,tr,ratio,&a,1.,1.,&d.error,error);
  double hmla=rec_HMLA_dxHIIdlna(&d,.00025,.00024,.0001,1e-16,ratio*tr,tr);
  double tla=rec_TLA_dxHIIdlna(&c,.00025,.00024,.0001,1e-16,ratio*tr,tr,1.);
  if(d.error){fprintf(stderr,"%s",error);return 5;}
  printf("%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g\n",aa[0],aa[1],da[0],da[1],bb[0],bb[1],r,hmla,tla);
 }
 return 0;
}
'''

NATIVE_FIXTURE=r'''
#define main unused_original_main
#include "q042_context_native_v29.c"
#undef main
static int fake_rhs(double s,double *y,double *dy,void *p,ErrorMsg err){
 struct thermodynamics_parameters_and_workspace *a=p;
 dy[0]=1.;dy[1]=0.;dy[2]=2.;
 a->ptw->ptdw->x_noreio=y[2]+a->ptw->fHe*y[1];
 a->ptw->ptrp->reionization_parameters[a->ptw->ptrp->index_re_xe_before]=a->ptw->ptdw->x_noreio;
 return _SUCCESS_;
}
int main(int argc,char **argv){
 struct background ba={0};struct precision pr={0};struct thermodynamics th={0};
 struct thermo_workspace w={0};struct thermo_diffeq_workspace d={0};struct thermo_vector v={0};
 struct thermohyrec hy={0};HYREC_DATA data={0};HYREC_ATOMIC at={0};REC_COSMOPARAMS cosmo={0};FIT_FUNC fit={0};
 struct thermo_reionization_parameters rp={0};struct thermodynamics_parameters_and_workspace a={0};
 a.pba=&ba;a.ppr=&pr;a.pth=&th;a.ptw=&w;w.ptdw=&d;w.ptrp=&rp;d.ptv=&v;d.phyrec=&hy;
 hy.data=&data;data.atomic=&at;data.cosmo=&cosmo;data.fit=&fit;hy.xHeII_limit=1e-6;
 double yy[3]={-86.955287923490403,1.2261504557092879e-5,.00024187860481588748};
 v.y=yy;v.ti_size=3;v.index_ti_D_Tmat=0;v.index_ti_x_He=1;v.index_ti_x_H=2;
 w.fHe=cosmo.fHe=.081556058814182833;w.Tcmb=2.7254999999999998;w.SIunit_nH0=.17567299793393323;
 cosmo.fsR=cosmo.meR=1.;th.tau_reio=.022146719553358576;th.recombination=hyrec;th.reio_parametrization=reio_camb;th.reio_z_or_tau=reio_tau;
 d.ap_current=d.index_ap_reio=1;d.index_ap_frec=0;d.require_H=d.require_He=1;
 double limits[2]={50.,0.},deltas[2]={.1,.1};d.ap_z_limits=limits;d.ap_z_limits_delta=deltas;
 pr.reionization_z_start_max=50;pr.reionization_start_factor=8;th.reionization_width=.5;th.helium_fullreio_redshift=3.5;th.helium_fullreio_width=.5;
 double re[9]={46,1.5,.5,0,1+w.fHe,w.fHe,3.5,.5,50};rp.reionization_parameters=re;rp.re_size=9;
 rp.index_re_reio_redshift=0;rp.index_re_reio_exponent=1;rp.index_re_reio_width=2;rp.index_re_xe_before=3;rp.index_re_xe_after=4;rp.index_re_helium_fullreio_fraction=5;rp.index_re_helium_fullreio_redshift=6;rp.index_re_helium_fullreio_width=7;rp.index_re_reio_start=8;
 double loga[2]={-4.,0.},back[4]={.001,1e-12,.001,1e-12},dd[4]={0};ba.bt_size=2;ba.bg_size=2;ba.index_bg_H=0;ba.index_bg_rho_g=1;ba.loga_table=loga;ba.background_table=back;ba.d2background_dloga2_table=dd;
 for(int l=0;l<4;l++){at.logAlpha_tab[l]=malloc(NTM*sizeof(double*));for(int m=0;m<NTM;m++){at.logAlpha_tab[l][m]=malloc(NTR*sizeof(double));for(int n=0;n<NTR;n++)at.logAlpha_tab[l][m][n]=-30.;}}
 for(int n=0;n<NTR;n++){at.logR2p2s_tab[n]=-2.;at.logTR_tab[n]=log(TR_MIN)+n*(log(TR_MAX)-log(TR_MIN))/(NTR-1);}
 for(int n=0;n<NTM;n++)at.T_RATIO_tab[n]=T_RATIO_MIN+n*.9/(NTM-1);
 at.DlogTR=at.logTR_tab[1]-at.logTR_tab[0];at.DT_RATIO=at.T_RATIO_tab[1]-at.T_RATIO_tab[0];
 double first[1]={1775.};fit.swift_func[0]=first;
 int size=28333;th.tt_size=size;th.th_size=3;th.index_th_xe=0;th.index_th_dkappa=1;th.index_th_dddkappa=2;
 th.z_table=malloc(size*sizeof(double));th.tau_table=malloc(size*sizeof(double));th.thermodynamics_table=calloc(size*3,sizeof(double));double *grid=malloc(size*sizeof(double));
 for(int i=0;i<size;i++){th.z_table[i]=50.*i/(size-1);th.tau_table[i]=10000.-i*.1;}
 for(int i=0;i<size;i++)grid[i]=-th.z_table[size-1-i];
 q042_states_allocate(size);q042_original_derivs=fake_rhs;q042_dir=argv[1];q042_run="SYNTHETIC_EXPORT_FIXTURE";q042_config=argv[2];q042_started=q042_now();
 return thermodynamics_reionization_evolve_with_tau(&a,-50.,0.,grid,size);
}
'''

def capture_fixture(root):
    import hashlib
    with tempfile.TemporaryDirectory(prefix='q042-export-fixture-') as td:
        td=Path(td);src=td/'fixture.c';src.write_text(NATIVE_FIXTURE);exe=td/'fixture'
        cmd=['gcc','-O2','-std=c99','-ffunction-sections','-fdata-sections','-fno-fast-math','-ffp-contract=off','-I'+str(Path(__file__).resolve().parent)]
        for p in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'): cmd+=['-I'+str(root/p)]
        cmd += [str(src),str(root/'external/HyRec2020/hydrogen.c'),str(root/'external/HyRec2020/hyrectools.c'),'-D_DEFAULT_SOURCE','-Wl,--gc-sections','-lm','-ldl','-o',str(exe)]
        subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=60)
        subprocess.run([str(exe),str(td),'0'*64],check=True,capture_output=True,text=True,timeout=30)
        ctx=json.loads((td/'initialized_context.json').read_text());gr=json.loads((td/'native_grid_hex.json').read_text())
        assert len(ctx['logAlpha'])==4 and len(ctx['logAlpha'][0])==40 and len(ctx['logAlpha'][0][0])==100
        assert all(float.fromhex(v)==-30 for a in ctx['logAlpha'] for row in a for v in row)
        assert len(ctx['logR'])==100 and all(float.fromhex(v)==-2 for v in ctx['logR'])
        assert len(gr['rows'])==28333
        assert [float.fromhex(x) for x in ctx['accepted_D_He_H']]==[-86.955287923490403,1.2261504557092879e-5,.00024187860481588748]
        assert float.fromhex(ctx['trials']['LOWER']['start'])==7.5 and float.fromhex(ctx['trials']['UPPER']['center'])==46
        assert float.fromhex(ctx['entry_reionization_parameters'][3])==.00024187860481588748+.081556058814182833*1.2261504557092879e-5
        assert len((td/'original_rhs_points.jsonl').read_text().splitlines())==24
        e=Evaluator(ctx);r=e.rhs(I(49.999,50),I(-86.956,-86.954),I(.0002418,.0002419),'UPPER')
        source=e.source_xe_dkappa(I(49.999,50),r['xe_noreio'],r['xe_reio'])
        return {'gate':'PASS_SYNTHETIC_EXPORT_ONLY','original_binary_used':False,'rows':28333,'serialized_logAlpha_values':16000,'restored_entry_scratch':'PASS','artifacts_sha256':{n:hashlib.sha256((td/n).read_bytes()).hexdigest() for n in ('initialized_context.json','native_grid_hex.json','original_rhs_points.jsonl')},'source_write_fixture':jsonable(source),'positivity_fixture':e.positivity()}

def fixture():
    k={'Tcmb':2.7255,'nH0':.17567299793393323,'fHe':.08155605881418283,'helium':1.2261504557092879e-5,'helium_cutoff':1e-6,'c':299792458.,'Mpc':3.085677581282e22,'sigma':6.6524616e-29,'me':9.10938215e-31,'Jm3':.0151730087,'cm3':1e-6,'kBoltz':8.617343e-5,'TR_MIN':.004,'TR_MAX':.4,'T_RATIO_MIN':.1,'SAHA':3.016103031869581e21,'LYA':4.662899067555897e15,'EI':13.598286071938324,'L2s':8.2206,'alpha_pref':4.309e-13,'alpha_pow1':-.6166,'alpha_den':.6703,'alpha_pow2':.53}
    flags=dict.fromkeys(['hyrec','reio_camb','no_exotic','no_varconst','no_idm','no_idr','no_idm_b','require_H','phase_reio','MODEL_SWIFT','hyrec_error_zero','fsR_meR_one'],True);flags['require_He']=False
    trials={name:{key:float(val).hex() for key,val in dict(center=center,start=start,exponent=1.5,width=.5,after=1+k['fHe'],he_fraction=k['fHe'],he_center=3.5,he_width=.5).items()} for name,center,start in [('UPPER',46,50),('LOWER',0,7.5)]}
    return {'q':'Q-042','program_id':'Q042-CONTEXT-V29','fixture_only':True,'constants':{name:float(x).hex() for name,x in k.items()},'flags':flags,'logAlpha':[[[(-30.+.01*l+.002*m-.005*n).hex() for n in range(100)] for m in range(40)] for l in range(4)],'logR':[(-2.-.01*n).hex() for n in range(100)],'DlogTR':(math.log(100)/99).hex(),'DT_RATIO':(.9/39).hex(),'background':[[float(x).hex() for x in row] for row in [(-4.,.001,1e-12,0.,0.),(0.,.001,1e-12,0.,0.)]],'fit_first_K':float(1775).hex(),'trials':trials}

def main(root,out):
    root=Path(root).resolve();out=Path(out);c=fixture();e=Evaluator(c)
    # Both table offsets, edge stencils and an interior stencil boundary.
    points=[(tr,ratio) for tr in [.004,.005,.01,.012] for ratio in [.1,.375,.999999,1.,1.000001,1.5]]
    tokens=[float.fromhex(c['DlogTR']),float.fromhex(c['DT_RATIO'])]+[float.fromhex(v) for p in c['logAlpha'] for r in p for v in r]+[float.fromhex(v) for v in c['logR']]+[v for p in points for v in p]
    with tempfile.TemporaryDirectory(prefix='q042-source-v29-') as td:
        src=Path(td)/'fixture.c';src.write_text(C_SOURCE);exe=Path(td)/'fixture'
        cmd=['gcc','-O2','-std=c99','-D_DEFAULT_SOURCE','-ffunction-sections','-fdata-sections','-fno-fast-math','-ffp-contract=off','-I'+str(root/'external/HyRec2020'),str(src),str(root/'external/HyRec2020/hydrogen.c'),str(root/'external/HyRec2020/hyrectools.c'),'-Wl,--gc-sections','-lm','-o',str(exe)]
        subprocess.run(cmd,check=True,timeout=60,capture_output=True,text=True)
        run=subprocess.run([str(exe)],input='\n'.join(format(v,'.17g') for v in tokens),capture_output=True,text=True,timeout=30,check=True)
    rows=[list(map(float,s.split())) for s in run.stdout.splitlines()]
    if len(rows)!=len(points): raise ValueError('SOURCE_FIXTURE_COMPLETENESS')
    report=[]
    for (tr,ratio),actual in zip(points,rows):
        # Nonzero domains: floating point containment is a diagnostic, not proof.
        ti=I(max(.004,tr-1e-10),tr+1e-10);ri=I(max(.1,ratio-1e-9),ratio+1e-9)
        rr,stencils=e.rates(ti,ri)
        hmla,_,_=e.hmla(I(.00025),I(.00024),I(.0001),I(1e-16),ti,ri)
        tla=e.tla(I(.00025),I(.00024),I(.0001),I(1e-16),ti*ri,ti)
        enclosures=rr+[hmla,tla]
        if len(actual)!=9 or not all(iv.contains(x) for iv,x in zip(enclosures,actual)): raise ValueError('PINNED_SOURCE_CONTAINMENT_DIAGNOSTIC '+str((tr,ratio)))
        report.append({'TR_eV':tr,'ratio':ratio,'original_C_output':actual,'enclosures':jsonable(enclosures),'stencils':stencils})
    # Explicit simultaneous wrapper/table/ratio and reionization boundaries.
    branch_checks=[]
    for z,rat in [(30,.1),(30,1.),(16.031010835587164,.2),(7.5,.2),(3.5,.2),(0,.2),(50,.375)]:
        zz=I(max(0,z-1e-8),min(50,z+1e-8));D=(rat-1)*2.7255*(1+z)
        for trial in ('UPPER','LOWER'):
            r=e.rhs(zz,I(D-1e-6,D+1e-6),I(.00024-1e-9,.00024+1e-9),trial)
            if rat==.1 or z==16.031010835587164:
                if len(r['branches'])!=2: raise ValueError('WRAPPER_BRANCH_COMPLETENESS')
            if rat==1. and {s[0] for s in r['stencils']}!={0,2}: raise ValueError('TABLE_OFFSET_COMPLETENESS')
            branch_checks.append({'z':z,'ratio':rat,'trial':trial,'output':jsonable(r)})
    result={'q':'Q-042','program_id':'Q042-CONTEXT-V29','gate':'PASS_SYNTHETIC_SOURCE_DIAGNOSTICS','scope':'24 pinned C rate/TLA/HMLA comparisons;14 synthetic RHS branch boxes; not actual initialization or binary-roundoff proof','cases':report,'branches':branch_checks,'positivity_fixture':e.positivity(),'capture_fixture':capture_fixture(root)}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'gate':result['gate'],'cases':len(report),'branch_boxes':len(branch_checks)}))

if __name__=='__main__':
    try: main(sys.argv[1],sys.argv[2])
    except subprocess.CalledProcessError as exc:
        print(exc.stdout or '',file=sys.stderr);print(exc.stderr or '',file=sys.stderr)
        raise
