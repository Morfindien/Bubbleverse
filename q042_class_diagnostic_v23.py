#!/usr/bin/env python3
"""One frozen-point CLASS attribution. No sampling or precision repair."""
from __future__ import annotations
import argparse, csv, hashlib, json, math, os, platform, subprocess, sys, sysconfig, time
from pathlib import Path

Q='Q-042';PROGRAM_ID='Q042-CLASSCAUSE-V23'
HERE=Path(__file__).resolve().parent
CLASS_COMMIT='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
ORIGINAL_BINARY='df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n')

def envelope(**values):
    return dict(q=Q,program_id=PROGRAM_ID,github_run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),
                execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),
                scientific_result=False,production_restart_authorized=False,new_bobyqa_starts=0,**values)

def spline_value(x0,x1,y0,y1,d0,d1,x):
    vals=(x0,x1,y0,y1,d0,d1,x)
    if not all(math.isfinite(v) for v in vals) or x1<=x0 or not x0<=x<=x1:
        raise ValueError('SPLINE_ARGUMENT_GATE=FAIL')
    h=x1-x0;b=(x-x0)/h;a=1-b
    return a*y0+b*y1+((a*a*a-a)*d0+(b*b*b-b)*d1)*h*h/6

def classify(left,right,value,method):
    if not all(math.isfinite(v) for v in (left,right,value)):raise ValueError('FINITE_DIAGNOSTIC_GATE=FAIL')
    if value>=0:return 'NEGATIVE_VALUE_NOT_REPRODUCED'
    if left<0 or right<0:return 'NEGATIVE_TABLE_NODE'
    return 'INTERPOLATION_OVERSHOOT' if method=='spline' else 'INCONSISTENT_LINEAR_RESULT'

def load_contract():
    c=json.loads((HERE/'q042_class_contract_v23.json').read_text())
    raw=c['preserved_class_result']['original_result']['raw_result']
    if (c['q'],c['program_id'],c['class_commit'],c['original_binary_sha256'])!=(Q,PROGRAM_ID,CLASS_COMMIT,ORIGINAL_BINARY):
        raise ValueError('CONTRACT_IDENTITY_GATE=FAIL')
    if c['parameters']!=raw['parameters'] or any(k in c['parameters'] for k in ('reionization_sampling','reio_parametrization')):
        raise ValueError('FROZEN_POINT_GATE=FAIL')
    if (c['maximum_distinct_points'],c['precision_changed'],c['production_restart_authorized'],c['new_bobyqa_starts'])!=(1,False,False,0):
        raise ValueError('FINITE_SCOPE_GATE=FAIL')
    return c

def validate_package(root):
    root=Path(root);m=json.loads((root/'q042_class_manifest_v23.json').read_text())
    if (m['q'],m['program_id'])!=(Q,PROGRAM_ID):raise ValueError('MANIFEST_IDENTITY_GATE=FAIL')
    for name,digest in m['files'].items():
        p=root/name
        if name=='q042-class-cause-v23.yml' and not p.exists():p=root/'.github/workflows'/name
        if not p.is_file() or sha(p)!=digest:raise ValueError('PACKAGE_HASH_GATE=FAIL '+name)
    if sha(root/'.github/workflows/00-bubbleverse-start.yml')!=m['permanent_launcher_sha256']:
        raise ValueError('PERMANENT_LAUNCHER_GATE=FAIL')
    registry=json.loads((root/'bubbleverse_program_registry.json').read_text())
    entry=registry['programs'].get(PROGRAM_ID,{})
    if (entry.get('q'),entry.get('status'),entry.get('workflow_id'),entry.get('target_ref'))!=(Q,'ACTIVE','q042-class-cause-v23.yml','main'):
        raise ValueError('LAUNCHER_GATE=FAIL')
    if not (root/'.github/workflows/q042-class-cause-v23.yml').is_file():raise ValueError('TARGET_PATH_GATE=FAIL')
    if registry['programs']['Q042-DURABLE-V22']['status']!='COMPLETED':raise ValueError('COMPLETED_V22_GATE=FAIL')
    text=(root/'README.md').read_text()
    if text.count('### Q-042 bounded CLASS cause diagnosis')!=1 or f'→ {PROGRAM_ID} →' not in text:
        raise ValueError('README_GATE=FAIL')
    c=json.loads((root/'q042_class_contract_v23.json').read_text())
    if sha(root/'q042_execution_handoff_v23.md')!=m['files']['q042_execution_handoff_v23.md'] or c['precision_changed']:
        raise ValueError('HANDOFF_CONTRACT_GATE=FAIL')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')

def point_ini(c,path):
    # Native parser accepts these same exact keys and values used by V20 classy.
    Path(path).write_text(''.join(f'{k} = {v}\n' for k,v in sorted(c['parameters'].items())))

def inspect_tables(out):
    out=Path(out);meta=json.loads((out/'native_meta.json').read_text());p=json.loads((out/'native_probe.json').read_text())
    with (out/'native_nodes.csv').open() as f:rows=[{k:float(v) for k,v in row.items()} for row in csv.DictReader(f)]
    if len(rows)!=meta['tt_size'] or any(not math.isfinite(v) for row in rows for v in row.values()):
        raise ValueError('TABLE_COMPLETENESS_GATE=FAIL')
    if any(a['z']>=b['z'] for a,b in zip(rows,rows[1:])):raise ValueError('TABLE_ORDER_GATE=FAIL')
    idx=p['last_index']
    if not 0<=idx<len(rows)-1:raise ValueError('INTERVAL_INDEX_GATE=FAIL')
    left,right=rows[idx:idx+2];details={}
    for col,dd in [('xe','d2xe_dz2'),('dkappa','d2dkappa_dz2')]:
        reconstructed=spline_value(left['z'],right['z'],left[col],right[col],left[dd],right[dd],p['z']) if p['method']=='spline' else left[col]+(right[col]-left[col])*(p['z']-left['z'])/(right['z']-left['z'])
        # Roundoff comparison only, NOT a prediction or likelihood tolerance.
        bound=1024*sys.float_info.epsilon*max(abs(left[col]),abs(right[col]),abs(reconstructed),1e-300)
        if abs(reconstructed-p[col])>bound:raise ValueError('NATIVE_INTERPOLATION_IDENTITY_GATE=FAIL '+col)
        details[col]=dict(diagnosis=classify(left[col],right[col],p[col],p['method']),left_node=left[col],right_node=right[col],native_value=p[col],reconstructed_value=reconstructed,roundoff_bound=bound)
    with (out/'native_extrema.csv').open() as f:
        extrema=[dict(interval=int(r['interval']),column=r['column'],**{k:float(r[k]) for k in ('z','xe','dkappa')}) for r in csv.DictReader(f)]
    if any(not math.isfinite(r[k]) for r in extrema for k in ('z','xe','dkappa')):raise ValueError('EXTREMA_FINITE_GATE=FAIL')
    # Verify every archived analytic candidate against the independent scalar
    # reconstruction, using the actual stored second derivatives.
    for r in extrema:
        a,b=rows[r['interval']:r['interval']+2]
        for col,dd in [('xe','d2xe_dz2'),('dkappa','d2dkappa_dz2')]:
            v=spline_value(a['z'],b['z'],a[col],b[col],a[dd],b[dd],r['z'])
            scale=max(abs(a[col]),abs(b[col]),abs(v),abs(a[dd])*(b['z']-a['z'])**2,abs(b[dd])*(b['z']-a['z'])**2,1e-300)
            if abs(v-r[col])>1024*sys.float_info.epsilon*scale:raise ValueError('EXTREMA_NATIVE_IDENTITY_GATE=FAIL')
    minima={col:min([{'z':r['z'],'value':r[col]} for r in rows if r['z']<=meta['reionization_z_start_max']]+[{'z':r['z'],'value':r[col]} for r in extrema],key=lambda x:x['value']) for col in ('xe','dkappa')}
    supported=all(v['diagnosis']=='INTERPOLATION_OVERSHOOT' for v in details.values())
    return dict(metadata=meta,probe=p,bracket=[left,right],details=details,
                causal_gate='PASS' if supported else 'UNRESOLVED',causal_statement='Positive bracketing table nodes become negative in the original spline interpolation.' if supported else 'The reported negative value is not explained as positive-node spline overshoot by this diagnostic.',
                table_rows=len(rows),minimum_node_xe=min(r['xe'] for r in rows),minimum_node_dkappa=min(r['dkappa'] for r in rows),reionization_range_minima=minima,extrema_count=len(extrema),
                reported_redshift_precision='Rounded original exception; not the exact unrounded perturbation query',
                precision_candidate_gate='BLOCKED_MISSING_PREREGISTERED_REFERENCE_AND_PREDICTION_LIKELIHOOD_TOLERANCES',
                class_blocker_resolved=False,original_perturbation_replayed=False)

def diagnose(out,class_root):
    c=load_contract();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False)
    root=Path(class_root).resolve()
    result=envelope(diagnostic_gate='FAIL',class_blocker_resolved=False,final_result_gate='UNRESOLVED')
    started=time.monotonic()
    try:
        commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
        if commit!=CLASS_COMMIT:raise ValueError('CLASS_COMMIT_GATE=FAIL')
        subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
        binaries=[p for p in root.rglob('classy*.so') if sha(p)==ORIGINAL_BINARY]
        if len(binaries)!=1:raise ValueError('ORIGINAL_CLASS_BINARY_GATE=FAIL expected exactly one matching frozen binary')
        binary=binaries[0]
        libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
        if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib:raise ValueError('PYTHON_LINK_GATE=FAIL')
        compiler=['gcc','-O2','-fopenmp']
        for p in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):compiler.extend(['-I',str(root/p)])
        exe=out/'q042_native_probe_v23'
        compiler += [str(HERE/'q042_class_probe_v23.c'),str(binary),'-L'+libdir,'-l'+ldlib.removeprefix('lib').split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-lm','-o',str(exe)]
        with (out/'compile.log').open('w') as f:subprocess.run(compiler,check=True,stdout=f,stderr=subprocess.STDOUT,timeout=c['compile_seconds'])
        point_ini(c,out/'point.ini')
        env=dict(os.environ,Q042_TRACE_DIR=str(out))
        with (out/'native.log').open('w') as f:subprocess.run([str(exe),str(out/'point.ini')],env=env,check=True,stdout=f,stderr=subprocess.STDOUT,timeout=c['point_seconds'])
        result.update(inspect_tables(out),diagnostic_gate='PASS',native_executable_sha256=sha(exe),native_compile_command=compiler,
                      binary_route=str(binary),class_binary_sha256=sha(binary),class_commit=commit,source_tree_gate='PASS',parameters=c['parameters'],
                      python_version=platform.python_version(),compiler_version=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
                      thread_environment={k:os.environ.get(k,'NOT DOCUMENTED') for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS')},
                      files={p.name:sha(p) for p in out.iterdir() if p.is_file()},precision_changed=False)
    except Exception as exc:result.update(exception_type=type(exc).__name__,exception=str(exc))
    result['elapsed_seconds']=time.monotonic()-started
    write(out/'q042_class_result_v23.json',result)
    if result['diagnostic_gate']!='PASS':raise ValueError('CLASS_DIAGNOSTIC_GATE=FAIL failure record preserved')

def collect_records(records,run_id,commit):
    valid=len(records)==1 and all((r.get('q'),r.get('program_id'),r.get('github_run_id'),r.get('execution_commit'),r.get('diagnostic_gate'),r.get('scientific_result'))==(Q,PROGRAM_ID,str(run_id),commit,'PASS',False) for r in records)
    valid=valid and all(r.get('class_binary_sha256')==ORIGINAL_BINARY and r.get('class_commit')==CLASS_COMMIT and r.get('production_restart_authorized') is False and r.get('precision_changed') is False and r.get('new_bobyqa_starts')==0 for r in records)
    return envelope(execution_status='DIAGNOSTIC_COMPLETE' if valid else 'DIAGNOSTIC_INCOMPLETE',job_completeness_gate='PASS' if valid else 'FAIL',technical_gate='PASS' if valid else 'FAIL',final_result_gate='UNRESOLVED',class_blocker_resolved=False,records=records)

def collect(source,out):
    paths=sorted(Path(source).rglob('q042_class_result_v23.json'))
    records=[];errors=[]
    for p in paths:
        try:
            r=json.loads(p.read_text());records.append(r)
            for name,digest in r.get('files',{}).items():
                if Path(name).name!=name or sha(p.parent/name)!=digest:raise ValueError('RAW_MEMBER_HASH_GATE=FAIL')
            if r.get('diagnostic_gate')=='PASS':
                native=inspect_tables(p.parent)
                for key,value in native.items():
                    if r.get(key)!=value:raise ValueError('NATIVE_RESULT_RECONSTRUCTION_GATE=FAIL '+key)
        except Exception as e:errors.append(dict(file=str(p),error=str(e)))
    result=collect_records(records,os.environ.get('GITHUB_RUN_ID','LOCAL'),os.environ.get('GITHUB_SHA','NOT DOCUMENTED'))
    if errors:result.update(job_completeness_gate='FAIL',technical_gate='FAIL',execution_status='DIAGNOSTIC_INCOMPLETE')
    result['read_errors']=errors;write(out,result)
    if result['job_completeness_gate']!='PASS':raise ValueError('DIAGNOSTIC_COMPLETENESS_GATE=FAIL final failure record preserved')

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('static','diagnose','collect'));p.add_argument('--root',default='.');p.add_argument('--class-root',default='external/class_ede');p.add_argument('--out',default='diag_results');p.add_argument('--source',default='collected');a=p.parse_args()
    if a.command=='static':load_contract();validate_package(a.root)
    elif a.command=='diagnose':diagnose(a.out,a.class_root)
    else:collect(a.source,a.out)

if __name__=='__main__':main()
