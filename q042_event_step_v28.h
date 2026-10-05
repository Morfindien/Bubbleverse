#ifndef Q042_EVENT_STEP_V28_H
#define Q042_EVENT_STEP_V28_H
#include <math.h>
#include <stddef.h>
typedef int (*q042_event_rhs)(double logical_s,double eval_s,const double y[2],double f[2],int stage,void *ctx);
/* s=-z increases. Only the terminal pre-event k4 samples nextafter(end,-inf).
 * The propagated state remains at the logical endpoint. Post k1 uses exact end.
 * This is a numerical one-sided evaluation convention, never a branch override. */
static int q042_event_step(double begin,double end,int pre_terminal,double y[2],q042_event_rhs rhs,void *ctx){
 double h=end-begin,k[4][2],u[2],accepted[2];
 if(!(h>0.)||!isfinite(h))return 1;
 for(int a=0;a<4;a++){
  double s=a==0?begin:a==3?end:begin+.5*h;
  for(int j=0;j<2;j++)u[j]=a==0?y[j]:y[j]+h*(a==3?1.:.5)*k[a==3?2:a-1][j];
  for(int j=0;j<2;j++)if(!isfinite(u[j]))return 1;
  double eval=(pre_terminal&&a==3)?nextafter(end,-INFINITY):s;
  if(rhs(s,eval,u,k[a],a+1,ctx))return 1;
  for(int j=0;j<2;j++)if(!isfinite(k[a][j]))return 1;
 }
 for(int j=0;j<2;j++){
  accepted[j]=y[j]+h*(k[0][j]+2*k[1][j]+2*k[2][j]+k[3][j])/6.;
  if(!isfinite(accepted[j]))return 1;
 }
 for(int j=0;j<2;j++)y[j]=accepted[j];
 return 0;
}
#endif
