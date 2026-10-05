#!/usr/bin/env python3
"""Q-042: one read-only original-binary tau/table-origin observation."""
import argparse, hashlib, importlib.util, json, math, os, platform, subprocess, sys, sysconfig, time
from pathlib import Path
Q='Q-042';PROGRAM_ID='Q042-CLASSORIGIN-V24';HERE=Path(__file__).resolve().parent
CLASS_COMMIT='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
BINARY_SHA='df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n')
def envelope(**extra):
    return dict(q=Q,program_id=PROGRAM_ID,github_run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),scientific_result=False,production_restart_authorized=False,new_bobyqa_starts=0,precision_changed=False,final_result_gate='UNRESOLVED',class_blocker_resolved=False,**extra)

def summarize_trace(events,expected_tau):
    grouped={k:[e for e in events if e.get('event')==k] for k in ('input','tau_enter','get_tau','tau_exit','final')}
    if any(len(grouped[k])!=1 for k in ('input','tau_enter','tau_exit','final')):raise ValueError('TRACE_EVENT_COMPLETENESS_GATE=FAIL')
    i=grouped['input'][0];en=grouped['tau_enter'][0];ex=grouped['tau_exit'][0];f=grouped['final'][0];g=grouped['get_tau']
    if i.get('reio_z_or_tau')!=1 or i.get('tau_reio')!=expected_tau or en.get('requested_tau')!=expected_tau:raise ValueError('FROZEN_TAU_INPUT_GATE=FAIL')
    if len(g)<2 or [e.get('call') for e in g]!=list(range(1,len(g)+1)):raise ValueError('TAU_TRIAL_SEQUENCE_GATE=FAIL')
    if f.get('tau_calls')!=1 or f.get('get_tau_calls')!=len(g) or f.get('source_calls',0)<=0 or f.get('trace_overflow') is not False or len(events)>256:raise ValueError('INTERPOSITION_OBSERVATION_GATE=FAIL')
    if ex.get('status')!=0 or any(e.get('status')!=0 for e in g):raise ValueError('ORIGINAL_CALL_RETURN_GATE=FAIL')
    if not (events[0] is i and events[-1] is f and events.index(en)<events.index(g[0])<events.index(g[-1])<events.index(ex)):raise ValueError('TRACE_ORDER_GATE=FAIL')
    bracket=[e.get('computed_tau') for e in g[:2]]
    def valid(x):return (isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)) or x in ('NaN','Infinity','-Infinity')
    if not all(valid(v) for v in bracket):raise ValueError('TAU_VALUE_ENCODING_GATE=FAIL')
    finite=all(isinstance(v,(int,float)) and math.isfinite(v) for v in bracket)
    return dict(trace_gate='PASS',tau_bracket=bracket,bracket_finite=finite,bisection_iterations=len(g)-2,
                mechanism='NONFINITE_BRACKET_WITH_ZERO_BISECTION_ITERATIONS' if not finite and len(g)==2 else 'OTHER_OBSERVED_TAU_PATH',
                requested_tau=expected_tau,last_computed_tau=g[-1]['computed_tau'],tau_exit=ex,
                scientific_result=False,production_restart_authorized=False,class_blocker_resolved=False)

def contract():
    c=json.loads((HERE/'q042_class_origin_contract_v24.json').read_text())
    if (c['q'],c['program_id'],c['source_commit'],c['original_binary_sha256'])!=(Q,PROGRAM_ID,CLASS_COMMIT,BINARY_SHA):raise ValueError('CONTRACT_IDENTITY_GATE=FAIL')
    if c['parameters']!=c['preserved_v23_result']['records'][0]['parameters'] or c['maximum_distinct_cosmologies']!=1 or c['precision_changed'] or c['scientific_result'] or c['production_restart_authorized'] or c['new_bobyqa_starts']!=0:raise ValueError('FROZEN_SCOPE_GATE=FAIL')
    return c
def parent_module():
    spec=importlib.util.spec_from_file_location('q042_parent',HERE/'q042_class_diagnostic_v23.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def static(root):
    c=contract();root=Path(root);m=json.loads((root/'q042_class_origin_manifest_v24.json').read_text())
    if (m['q'],m['program_id'])!=(Q,PROGRAM_ID):raise ValueError('MANIFEST_GATE=FAIL')
    for name,digest in m['files'].items():
        p=root/name
        if name.endswith('.yml') and not p.exists():p=root/'.github/workflows'/name
        if not p.is_file() or sha(p)!=digest:raise ValueError('PACKAGE_HASH_GATE=FAIL '+name)
    if sha(root/'.github/workflows/00-bubbleverse-start.yml')!=m['permanent_launcher_sha256']:raise ValueError('PERMANENT_LAUNCHER_GATE=FAIL')
    reg=json.loads((root/'bubbleverse_program_registry.json').read_text())['programs'];r=reg.get(PROGRAM_ID,{})
    if (r.get('q'),r.get('status'),r.get('workflow_id'),r.get('target_ref'))!=(Q,'ACTIVE','q042-class-origin-v24.yml','main') or reg['Q042-CLASSCAUSE-V23']['status']!='COMPLETED':raise ValueError('REGISTRY_GATE=FAIL')
    if not (root/'.github/workflows/q042-class-origin-v24.yml').is_file():raise ValueError('TARGET_GATE=FAIL')
    text=(root/'README.md').read_text()
    if text.count('### Q-042 bounded CLASS table-origin trace')!=1 or f'→ {PROGRAM_ID} →' not in text:raise ValueError('README_GATE=FAIL')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')
def observe(out,class_root):
    c=contract();p=parent_module();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);root=Path(class_root).resolve();r=envelope(trace_gate='FAIL');start=time.monotonic()
    try:
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=CLASS_COMMIT:raise ValueError('CLASS_COMMIT_GATE=FAIL')
        subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
        binaries=[b for b in root.rglob('classy*.so') if sha(b)==BINARY_SHA]
        if len(binaries)!=1:raise ValueError('ORIGINAL_CLASS_BINARY_GATE=FAIL')
        binary=binaries[0];libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
        if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib:raise ValueError('PYTHON_LINK_GATE=FAIL')
        exe=out/'q042_native_origin_probe_v24';cmd=['gcc','-O2','-fopenmp','-rdynamic']
        for sub in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):cmd+=['-I',str(root/sub)]
        cmd += [str(HERE/'q042_class_origin_probe_v24.c'),str(binary),'-L'+libdir,'-l'+ldlib.removeprefix('lib').split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        with (out/'compile.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        p.point_ini(c,out/'point.ini');env=dict(os.environ,Q042_TRACE_DIR=str(out))
        with (out/'native.log').open('w') as log:subprocess.run([str(exe),str(out/'point.ini')],env=env,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=c['runtime_seconds'])
        events=[json.loads(line) for line in (out/'native_trace.jsonl').read_text().splitlines()]
        summary=summarize_trace(events,c['parameters']['tau_reio']);inspection=p.inspect_tables(out)
        matches={n:sha(out/n)==digest for n,digest in c['unchanged_v23_raw_hashes'].items()}
        if not all(matches.values()):raise ValueError('OBSERVATIONAL_TABLE_IDENTITY_GATE=FAIL')
        r.update(summary,events=events,native_inspection=inspection,unchanged_v23_raw_products=matches,class_binary_sha256=sha(binary),class_commit=CLASS_COMMIT,source_tree_gate='PASS',binary_route=str(binary),native_executable_sha256=sha(exe),compile_command=cmd,parameters=c['parameters'],python_version=platform.python_version(),compiler_version=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],files={f.name:sha(f) for f in out.iterdir() if f.is_file()})
    except Exception as e:r.update(exception_type=type(e).__name__,exception=str(e))
    r['elapsed_seconds']=time.monotonic()-start;write(out/'q042_class_origin_result_v24.json',r)
    if r['trace_gate']!='PASS':raise ValueError('CLASS_ORIGIN_TRACE_GATE=FAIL failure record preserved')
def collect(source,out):
    c=contract();p=parent_module();records=[];errors=[]
    for f in sorted(Path(source).rglob('q042_class_origin_result_v24.json')):
        try:
            r=json.loads(f.read_text());records.append(r)
            for name,digest in r.get('files',{}).items():
                if Path(name).name!=name or sha(f.parent/name)!=digest:raise ValueError('RAW_MEMBER_HASH_GATE=FAIL')
            events=[json.loads(line) for line in (f.parent/'native_trace.jsonl').read_text().splitlines()]
            summary=summarize_trace(events,c['parameters']['tau_reio'])
            if r.get('events')!=events or any(r.get(k)!=v for k,v in summary.items()):raise ValueError('RAW_TRACE_RECONSTRUCTION_GATE=FAIL')
            if r.get('native_inspection')!=p.inspect_tables(f.parent):raise ValueError('TABLE_RECONSTRUCTION_GATE=FAIL')
            if any(sha(f.parent/n)!=digest for n,digest in c['unchanged_v23_raw_hashes'].items()):raise ValueError('TABLE_IDENTITY_GATE=FAIL')
        except Exception as e:errors.append({'file':str(f),'error':str(e)})
    expected=(Q,PROGRAM_ID,str(os.environ.get('GITHUB_RUN_ID','LOCAL')),os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),BINARY_SHA,CLASS_COMMIT,'PASS',False,False,False,0)
    valid=len(records)==1 and not errors and all(tuple(r.get(k) for k in ('q','program_id','github_run_id','execution_commit','class_binary_sha256','class_commit','trace_gate','scientific_result','production_restart_authorized','precision_changed','new_bobyqa_starts'))==expected for r in records)
    result=envelope(execution_status='DIAGNOSTIC_COMPLETE' if valid else 'DIAGNOSTIC_INCOMPLETE',technical_gate='PASS' if valid else 'FAIL',job_completeness_gate='PASS' if valid else 'FAIL',records=records,read_errors=errors)
    write(out,result)
    if not valid:raise ValueError('DIAGNOSTIC_COMPLETENESS_GATE=FAIL failure record preserved')
def main():
    a=argparse.ArgumentParser();a.add_argument('command',choices=('static','observe','collect'));a.add_argument('--root',default='.');a.add_argument('--class-root',default='external/class_ede');a.add_argument('--out',default='diag_results');a.add_argument('--source',default='collected');x=a.parse_args()
    if x.command=='static':static(x.root)
    elif x.command=='observe':observe(x.out,x.class_root)
    else:collect(x.source,x.out)
if __name__=='__main__':main()
