/* Independent known integrals catch endpoint contamination, restart discontinuity,
 * missing stages, wrong weights, nonfinite propagation and ignored RHS failure. */
#include "q042_event_step_v28.h"
#include <stdio.h>
#include <stdlib.h>
typedef struct {int calls,fail,mode;double last_eval,last_state;} fixture;
static int rhs(double s,double eval,const double y[2],double f[2],int stage,void *p){
 fixture*c=p;(void)s;(void)stage;c->calls++;c->last_eval=eval;c->last_state=y[0];
 if(c->fail&&c->calls==2)return 1;
 if(c->mode==0){f[0]=eval>=0.?1.:0.;f[1]=f[0];}
 else if(c->mode==1){f[0]=4*eval*eval*eval;f[1]=1.;}
 else if(c->mode==2){f[0]=y[0];f[1]=y[1];}
 else {f[0]=NAN;f[1]=1.;}
 return 0;
}
static void check(int ok,const char*msg){if(!ok){fprintf(stderr,"FAIL: %s\n",msg);exit(1);}}
int main(void){
 double y[2]={0,0};fixture c={0};
 check(!q042_event_step(-1.,0.,1,y,rhs,&c),"pre step must execute");
 check(y[0]==0.,"pre terminal k4 contaminated by exact-threshold post branch");
 check(c.calls==4&&c.last_eval<0.,"four stages, one-sided endpoint");
 check(!q042_event_step(0.,1.,0,y,rhs,&c)&&y[0]==1.&&y[1]==1.,"post restart uses same propagated state and original threshold branch");
 c=(fixture){0};y[0]=y[1]=0.;check(!q042_event_step(-1.,0.,0,y,rhs,&c)&&fabs(y[0]-1./6.)<1e-16,"naive aligned control must expose hJ/6");
 c=(fixture){.mode=1};y[0]=y[1]=0.;check(!q042_event_step(0.,1.,0,y,rhs,&c)&&y[0]==1.&&y[1]==1.,"RK4 integrates cubic forcing exactly");
 double errors[3];
 for(int a=0,n=1;a<3;a++,n*=2){c=(fixture){.mode=2};y[0]=y[1]=1.;for(int j=0;j<n;j++)check(!q042_event_step((double)j/n,(double)(j+1)/n,0,y,rhs,&c),"smooth step");errors[a]=fabs(y[0]-exp(1.));}
 check(errors[0]/errors[1]>10.&&errors[1]/errors[2]>12.,"smooth RK4 refinement loses expected order");
 c=(fixture){.fail=1};y[0]=y[1]=7.;check(q042_event_step(0.,1.,0,y,rhs,&c)&&y[0]==7.&&c.calls==2,"failed RHS must stop and not accept a partial step");
 c=(fixture){.mode=3};check(q042_event_step(0.,1.,0,y,rhs,&c),"nonfinite derivative must reject step");
 check(q042_event_step(1.,0.,0,y,rhs,&c),"backward malformed segment rejected");
 puts("EVENT_NUMERICS_GATE=PASS exact jump, endpoint trap, smooth forcing, restart and failures");return 0;
}
