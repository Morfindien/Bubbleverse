/* Q-042 independent diagnostic stepping; no CLASS/NDF15 numerical routines. */
#ifndef Q042_REFERENCE_INTEGRATORS_V26_H
#define Q042_REFERENCE_INTEGRATORS_V26_H
#include <float.h>
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
typedef int (*q042_rhs)(double,const double*,double*,void*,char*,size_t);
typedef struct {unsigned long rhs_calls,steps;int max_newton_used;double max_scaled_residual,last_s,last_y[2],last_f[2];} q042_solver_stats;
static int q042_eval(q042_rhs rhs,double s,const double y[2],double f[2],void *ctx,q042_solver_stats *st,char *err,size_t n){
 st->last_s=s;st->last_y[0]=y[0];st->last_y[1]=y[1];st->last_f[0]=st->last_f[1]=NAN;
 if(!isfinite(s)||!isfinite(y[0])||!isfinite(y[1])){snprintf(err,n,"NONFINITE_STAGE");return 1;}
 st->rhs_calls++;
 f[0]=f[1]=NAN;
 int status=rhs(s,y,f,ctx,err,n);st->last_f[0]=f[0];st->last_f[1]=f[1];if(status)return 1;
 if(!isfinite(f[0])||!isfinite(f[1])){snprintf(err,n,"NONFINITE_RHS");return 1;}
 return 0;
}
static double q042_residual_norm(const double r[2],const double old[2],const double x[2]){
 const double atol[2]={1e-10,1e-14};double m=0;
 for(int j=0;j<2;j++){double a=fabs(r[j])/(atol[j]+1e-10*fmax(fabs(old[j]),fabs(x[j])));if(a>m)m=a;}
 return m;
}
static int q042_step(int method,double s,double h,const double y[2],double out[2],q042_rhs rhs,void *ctx,q042_solver_stats *st,char *err,size_t n){
 double k1[2],k2[2],k3[2],k4[2],x[2],tmp[2];
 if(method!=0&&method!=1){snprintf(err,n,"UNKNOWN_METHOD");return 1;}
 if(!isfinite(h)||h<0){snprintf(err,n,"INVALID_STEP");return 1;}
 if(h==0){out[0]=y[0];out[1]=y[1];return 0;}
 if(q042_eval(rhs,s,y,k1,ctx,st,err,n))return 1;
 if(method==0){
  for(int j=0;j<2;j++)tmp[j]=y[j]+.5*h*k1[j];
  if(q042_eval(rhs,s+.5*h,tmp,k2,ctx,st,err,n))return 1;
  for(int j=0;j<2;j++)tmp[j]=y[j]+.5*h*k2[j];
  if(q042_eval(rhs,s+.5*h,tmp,k3,ctx,st,err,n))return 1;
  for(int j=0;j<2;j++)tmp[j]=y[j]+h*k3[j];
  if(q042_eval(rhs,s+h,tmp,k4,ctx,st,err,n))return 1;
  for(int j=0;j<2;j++)x[j]=y[j]+h*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6;
 }else{
  for(int j=0;j<2;j++)x[j]=y[j]+h*k1[j];
  for(int it=1;it<=12;it++){
   double r[2],J[2][2],mid[2],f[2];
   if(it>st->max_newton_used)st->max_newton_used=it;
   for(int j=0;j<2;j++)mid[j]=.5*(y[j]+x[j]);
   if(q042_eval(rhs,s+.5*h,mid,f,ctx,st,err,n))return 1;
   for(int j=0;j<2;j++)r[j]=x[j]-y[j]-h*f[j];
   double norm=q042_residual_norm(r,y,x);
   if(!isfinite(norm)){snprintf(err,n,"NONFINITE_NEWTON_RESIDUAL");return 1;}
   if(norm<=1){if(norm>st->max_scaled_residual)st->max_scaled_residual=norm;goto converged;}
   const double scale[2]={100.,1e-3};
   for(int k=0;k<2;k++){
    double plus[2]={mid[0],mid[1]},minus[2]={mid[0],mid[1]},fp[2],fm[2];
    double delta=sqrt(DBL_EPSILON)*fmax(fabs(mid[k]),scale[k]);
    plus[k]+=delta;minus[k]-=delta;
    if(q042_eval(rhs,s+.5*h,plus,fp,ctx,st,err,n)||q042_eval(rhs,s+.5*h,minus,fm,ctx,st,err,n))return 1;
    for(int j=0;j<2;j++)J[j][k]=(j==k?1.:0.)-.5*h*(fp[j]-fm[j])/(2*delta);
   }
   double det=J[0][0]*J[1][1]-J[0][1]*J[1][0];
   if(!isfinite(det)||fabs(det)<=DBL_EPSILON*fmax(1.,fabs(J[0][0]*J[1][1])+fabs(J[0][1]*J[1][0]))){snprintf(err,n,"SINGULAR_MIDPOINT_JACOBIAN");return 1;}
   double dx[2]={(J[1][1]*r[0]-J[0][1]*r[1])/det,(-J[1][0]*r[0]+J[0][0]*r[1])/det};
   for(int j=0;j<2;j++)x[j]-=dx[j];
  }
  snprintf(err,n,"MIDPOINT_NEWTON_CAP");return 1;
 }
 converged:
 if(!isfinite(x[0])||!isfinite(x[1])){snprintf(err,n,"NONFINITE_STEP");return 1;}
 out[0]=x[0];out[1]=x[1];st->steps++;return 0;
}
#endif
