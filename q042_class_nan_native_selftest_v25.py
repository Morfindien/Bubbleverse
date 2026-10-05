"""Compile and run the real observer wrappers against a controlled boundary dependency.
This tests unchanged forwarding and finite-to-NaN telemetry; it is not CLASS execution.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

def run(headers):
    here=Path(__file__).resolve().parent;headers=Path(headers).resolve()
    include=[]
    for d in ['include','external/HyRec2020','external/RecfastCLASS','external/heating']:include+=['-I',str(headers/d)]
    fixture=r'''
#include "class.h"
#include <dlfcn.h>
#include <assert.h>
static FILE *trace_file;
static unsigned trace_events,get_tau_calls;
static int trace_overflow,tau_active=1;
static void number(double x){if(isnan(x))fputs("\"NaN\"",trace_file);else if(isinf(x))fputs(x>0?"\"Infinity\"":"\"-Infinity\"",trace_file);else fprintf(trace_file,"%.17g",x);}
static int event(void){if(trace_events>=256){trace_overflow=1;return 0;}trace_events++;return 1;}
static int calls;
static double *seen_output;
static struct thermodynamics *seen_th;
static int dependency(struct thermodynamics *th,struct thermohyrec *hy,double xH,double xHe,double xe,double nH,double z,double Hz,double Tm,double Tr,double alpha,double me,double *out){
  calls++;seen_output=out;seen_th=th;assert(xH==0.0002&&xHe==0&&xe==0.0002&&nH==1&&Hz==2&&Tm==3&&Tr==4&&alpha==1&&me==1);
  *out=calls==1?0.1:NAN;return 0;
}
static void *original(const char *name){assert(strcmp(name,"hyrec_dx_H_dz")==0);return (void*)dependency;}
#include "q042_class_nan_observers_v25.h"
int main(void){
  struct thermodynamics th={0};double out;
  trace_file=stdout;
  assert(hyrec_dx_H_dz(&th,NULL,0.0002,0,0.0002,1,50,2,3,4,1,1,&out)==0&&out==0.1);
  assert(hyrec_dx_H_dz(&th,NULL,0.0002,0,0.0002,1,49,2,3,4,1,1,&out)==0&&isnan(out));
  assert(hyrec_dx_H_dz(&th,NULL,0.0002,0,0.0002,1,48,2,3,4,1,1,&out)==0&&isnan(out));
  assert(calls==3&&seen_output==&out&&seen_th==&th&&upstream_calls[3]==3&&!trace_overflow&&!upstream_schema_error);
  return 0;
}
'''
    with tempfile.TemporaryDirectory() as d:
        d=Path(d);p=d/'fixture.c';p.write_text(fixture);exe=d/'fixture'
        compiled=subprocess.run(['gcc','-O2','-Wall','-Wextra','-Wno-unused-parameter','-Wno-unused-function',*include,'-I',str(here),str(p),'-lm','-ldl','-o',str(exe)],capture_output=True,text=True)
        if compiled.returncode or compiled.stderr:raise AssertionError('Observer fixture compile failed or warned: '+compiled.stderr)
        result=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
        rows=[json.loads(x) for x in result.stdout.splitlines()]
        bad=[x for x in rows if x['kind']=='first_nonfinite']
        assert len(bad)==1 and bad[0]['phase']=='exit' and bad[0]['inputs_finite'] and not bad[0]['outputs_finite']
        assert bad[0]['outputs']=={'dx_H_dz':'NaN'} and bad[0]['previous_finite']['call']==1 and bad[0]['previous_finite']['outputs']=={'dx_H_dz':0.1}
        import importlib.util
        spec=importlib.util.spec_from_file_location('nan_controller',here/'q042_class_nan_v25.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        assert mod.classify_upstream(rows)['diagnosis']=='FINITE_INPUT_NONFINITE_OUTPUT_AT_OBSERVED_BOUNDARY'
        print('NATIVE_OBSERVER_SELFTEST=PASS (controlled dependency; no cosmology executed)')
        return rows
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'external/class_ede')
