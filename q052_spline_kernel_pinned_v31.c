#include <stdio.h>
#define _FAILURE_ 1
#define _SUCCESS_ 0
typedef char ErrorMsg[2048];
int array_interpolate_spline(
                             double * __restrict__ x_array,
                             int n_lines,
                             double * __restrict__ array,
                             double * __restrict__ array_splined,
                             int n_columns,
                             double x,
                             int * __restrict__ last_index,
                             double * __restrict__ result,
                             int result_size, /** from 1 to n_columns */
                             ErrorMsg errmsg) {

  int inf,sup,mid,i;
  double h,a,b;

  inf=0;
  sup=n_lines-1;

  if (x_array[inf] < x_array[sup]){

    if (x < x_array[inf]) {
      sprintf(errmsg,"%s(L:%d) : x=%e < x_min=%e",__func__,__LINE__,x,x_array[inf]);
      return _FAILURE_;
    }

    if (x > x_array[sup]) {
      sprintf(errmsg,"%s(L:%d) : x=%e > x_max=%e",__func__,__LINE__,x,x_array[sup]);
      return _FAILURE_;
    }

    while (sup-inf > 1) {

      mid=(int)(0.5*(inf+sup));
      if (x < x_array[mid]) {sup=mid;}
      else {inf=mid;}

    }

  }

  else {

    if (x < x_array[sup]) {
      sprintf(errmsg,"%s(L:%d) : x=%e < x_min=%e",__func__,__LINE__,x,x_array[sup]);
      return _FAILURE_;
    }

    if (x > x_array[inf]) {
      sprintf(errmsg,"%s(L:%d) : x=%e > x_max=%e",__func__,__LINE__,x,x_array[inf]);
      return _FAILURE_;
    }

    while (sup-inf > 1) {

      mid=(int)(0.5*(inf+sup));
      if (x > x_array[mid]) {sup=mid;}
      else {inf=mid;}

    }

  }

  *last_index = inf;

  h = x_array[sup] - x_array[inf];
  b = (x-x_array[inf])/h;
  a = 1-b;

  for (i=0; i<result_size; i++)
    *(result+i) =
      a * *(array+inf*n_columns+i) +
      b * *(array+sup*n_columns+i) +
      ((a*a*a-a)* *(array_splined+inf*n_columns+i) +
       (b*b*b-b)* *(array_splined+sup*n_columns+i))*h*h/6.;

  return _SUCCESS_;
}

