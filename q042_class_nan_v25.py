#!/usr/bin/env python3
"""One finite original-binary upstream observation, never a scientific repair."""
import argparse, hashlib, importlib.util, json, math, os, platform, subprocess, sysconfig, time
from pathlib import Path
Q='Q-042';PROGRAM_ID='Q042-CLASSNAN-V25';HERE=Path(__file__).resolve().parent
CLASS_COMMIT='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
BINARY_SHA='df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf'
BOUNDARIES=('thermodynamics_derivs','thermodynamics_ionization_fractions','thermodynamics_reionization_function','hyrec_dx_H_dz','hyrec_dx_He_dz')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n')
def envelope(**x):
    c=contract()
    return dict(q=Q,case_id=c['case_id'],scientific_question=c['scientific_question'],program_id=PROGRAM_ID,contract_sha256=sha(HERE/'q042_class_nan_contract_v25.json'),original_scientific_spec_sha256=c['original_scientific_spec_sha256'],github_run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),scientific_result=False,production_restart_authorized=False,new_bobyqa_starts=0,precision_changed=False,compiled_core_algorithm_changed=False,final_result_gate='UNRESOLVED',class_blocker_resolved=False,**x)
def module(name,file):
    s=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def contract():
    c=json.loads((HERE/'q042_class_nan_contract_v25.json').read_text())
    if (c['q'],c['program_id'],c['source_commit'],c['original_binary_sha256'])!=(Q,PROGRAM_ID,CLASS_COMMIT,BINARY_SHA):raise ValueError('CONTRACT_IDENTITY_GATE=FAIL')
    if c['parameters']!=c['preserved_v24_result']['records'][0]['parameters'] or c['maximum_distinct_cosmologies']!=1 or c['maximum_original_binary_observational_executions']!=1 or c['runtime_seconds']!=900:raise ValueError('FROZEN_POINT_GATE=FAIL')
    if any(c[k] for k in ('precision_changed','compiled_core_algorithm_changed','production_restart_authorized','scientific_result','new_bobyqa_starts','repair_execution_authorized')):raise ValueError('FROZEN_SCOPE_GATE=FAIL')
    return c
def finite_fields(fields):
    if not isinstance(fields,dict):raise ValueError('FIELD_SCHEMA_GATE=FAIL')
    finite=True
    for k,v in fields.items():
        if not isinstance(k,str):raise ValueError('FIELD_NAME_GATE=FAIL')
        if isinstance(v,bool) or v is None:raise ValueError('NUMBER_ENCODING_GATE=FAIL')
        if isinstance(v,(int,float)):
            if not math.isfinite(v):raise ValueError('NONFINITE_ENCODING_GATE=FAIL')
        elif isinstance(v,str) and v in ('NaN','Infinity','-Infinity'):finite=False
        else:raise ValueError('NUMBER_ENCODING_GATE=FAIL')
    return finite
def classify_upstream(events):
    rows=[e for e in events if e.get('event')=='upstream']
    if not rows:raise ValueError('UPSTREAM_INTERPOSITION_GATE=FAIL no observed upstream events')
    seen_bad=set();last={};bad=[]
    for e in rows:
        if e.get('boundary') not in BOUNDARIES or e.get('phase') not in ('entry','exit') or e.get('kind') not in ('initial','first_nonfinite'):raise ValueError('UPSTREAM_SCHEMA_GATE=FAIL')
        if type(e.get('trial')) is not int or e['trial']<1 or type(e.get('call')) is not int or e['call']<1 or type(e.get('status')) is not int:raise ValueError('UPSTREAM_CALL_GATE=FAIL')
        if not isinstance(e.get('z'),(int,float)) or isinstance(e['z'],bool) or not math.isfinite(e['z']):raise ValueError('REDSHIFT_GATE=FAIL')
        key=(e['trial'],e['boundary'],e['phase'])
        if e['call']<=last.get(key,0):raise ValueError('UPSTREAM_ORDER_GATE=FAIL')
        last[key]=e['call'];fi=finite_fields(e.get('inputs'));fo=finite_fields(e.get('outputs'))
        if not e['inputs'] or (e['phase']=='exit' and e['status']==0 and not e['outputs']):raise ValueError('SNAPSHOT_COMPLETENESS_GATE=FAIL')
        if type(e.get('inputs_finite')) is not bool or type(e.get('outputs_finite')) is not bool or (fi,fo)!=(e['inputs_finite'],e['outputs_finite']):raise ValueError('FINITE_FLAG_GATE=FAIL')
        previous=e.get('previous_finite')
        if previous is not None:
            if type(previous.get('call')) is not int or not 0<previous['call']<e['call'] or not finite_fields(previous.get('inputs')) or not finite_fields(previous.get('outputs')):raise ValueError('PREVIOUS_FINITE_GATE=FAIL')
            if not isinstance(previous.get('z'),(int,float)) or not math.isfinite(previous['z']):raise ValueError('PREVIOUS_REDSHIFT_GATE=FAIL')
        if e['kind']=='first_nonfinite':
            if fi and fo or key in seen_bad:raise ValueError('FIRST_NONFINITE_GATE=FAIL')
            seen_bad.add(key);bad.append(e)
        elif not fi or not fo:
            raise ValueError('INITIAL_FINITE_GATE=FAIL')
    first=bad[0] if bad else None
    diagnosis='NO_NONFINITE_OBSERVED_AT_INSTRUMENTED_BOUNDARIES'
    if first:
        if first['phase']=='entry':diagnosis='NONFINITE_PRESENT_ON_OBSERVED_ENTRY'
        elif first['inputs_finite'] and not first['outputs_finite']:diagnosis='FINITE_INPUT_NONFINITE_OUTPUT_AT_OBSERVED_BOUNDARY'
        else:diagnosis='NONFINITE_PROPAGATION_AT_OBSERVED_BOUNDARY'
    return dict(upstream_gate='PASS',diagnosis=diagnosis,first_observed=first,first_nonfinite_events=bad,upstream_event_count=len(rows),global_first_nonfinite_established=False,repair_ready=False,repair_readiness_gate='BLOCKED_PENDING_CAUSE_REFERENCE_TOLERANCE_AND_LINEAGE',scientific_result=False)

def summarize_trace(events,tau):
    # V24's proven input/order/counter gate is retained; extra upstream events are new evidence.
    v24=module('origin_v24','q042_class_origin_v24.py');s=v24.summarize_trace(events,tau)
    s.update(classify_upstream(events))
    finals=[e for e in events if e.get('event')=='final'];counts=finals[0].get('upstream_calls',{})
    if set(counts)!=set(BOUNDARIES) or any(type(n) is not int or n<0 for n in counts.values()) or any(counts[k]==0 for k in BOUNDARIES[:3]):raise ValueError('UPSTREAM_COUNTER_GATE=FAIL')
    for e in events:
        if e.get('event')=='upstream' and (e['call']>counts[e['boundary']] or e['trial']>finals[0]['get_tau_calls']):raise ValueError('UPSTREAM_COUNTER_GATE=FAIL')
    if finals[0].get('upstream_schema_error') is not False:raise ValueError('UPSTREAM_STATE_SCHEMA_GATE=FAIL')
    recombination=[e['inputs'].get('recombination') for e in events if e.get('event')=='upstream' and e.get('boundary')=='thermodynamics_derivs' and e.get('phase')=='entry']
    if 1 in recombination and (counts['hyrec_dx_H_dz']==0 or counts['hyrec_dx_He_dz']==0):raise ValueError('HYREC_INTERPOSITION_GATE=FAIL')
    return s

def collect_records(records,run_id,commit,errors):
    keys=('q','program_id','github_run_id','execution_commit','class_binary_sha256','class_commit','trace_gate','scientific_result','production_restart_authorized','precision_changed','new_bobyqa_starts')
    expected=(Q,PROGRAM_ID,str(run_id),commit,BINARY_SHA,CLASS_COMMIT,'PASS',False,False,False,0)
    valid=len(records)==1 and not errors and all(tuple(r.get(k) for k in keys)==expected for r in records)
    return envelope(execution_status='DIAGNOSTIC_COMPLETE' if valid else 'DIAGNOSTIC_INCOMPLETE',technical_gate='PASS' if valid else 'FAIL',job_completeness_gate='PASS' if valid else 'FAIL',records=records,read_errors=errors)

def static(root):
    c=contract();root=Path(root);m=json.loads((root/'q042_class_nan_manifest_v25.json').read_text())
    if (m['q'],m['program_id'])!=(Q,PROGRAM_ID):raise ValueError('MANIFEST_IDENTITY_GATE=FAIL')
    for name,digest in m['files'].items():
        p=root/name
        if name.endswith('.yml') and not p.exists():p=root/'.github/workflows'/name
        if not p.is_file() or sha(p)!=digest:raise ValueError('PACKAGE_HASH_GATE=FAIL '+name)
    if sha(root/'.github/workflows/00-bubbleverse-start.yml')!=m['permanent_launcher_sha256']:raise ValueError('LAUNCHER_HASH_GATE=FAIL')
    reg=json.loads((root/'bubbleverse_program_registry.json').read_text())['programs'];r=reg.get(PROGRAM_ID,{})
    if (r.get('q'),r.get('status'),r.get('workflow_id'),r.get('target_ref'),r.get('program_version'),r.get('workflow_version'))!=(Q,'ACTIVE','q042-class-nan-v25.yml','main',25,25):raise ValueError('REGISTRY_GATE=FAIL')
    if reg['Q042-CLASSORIGIN-V24'].get('status')!='COMPLETED' or reg['Q042-CLASSORIGIN-V24'].get('completion_run_id')!=37275520455:raise ValueError('COMPLETED_PARENT_GATE=FAIL')
    if not (root/'.github/workflows/q042-class-nan-v25.yml').is_file():raise ValueError('TARGET_GATE=FAIL')
    readme=(root/'README.md').read_text()
    if readme.count('### Q-042 bounded upstream CLASS nonfinite trace')!=1 or f'→ {PROGRAM_ID} →' not in readme:raise ValueError('README_GATE=FAIL')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')

def observe(out,class_root):
    c=contract();p=module('attribution_v23','q042_class_diagnostic_v23.py');out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);root=Path(class_root).resolve();r=envelope(trace_gate='FAIL');start=time.monotonic()
    try:
        if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1':raise ValueError('NO_RETRY_GATE=FAIL')
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=CLASS_COMMIT:raise ValueError('CLASS_COMMIT_GATE=FAIL')
        subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
        binaries=[b for b in root.rglob('classy*.so') if sha(b)==BINARY_SHA]
        if len(binaries)!=1:raise ValueError('ORIGINAL_BINARY_GATE=FAIL')
        binary=binaries[0];libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
        if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib:raise ValueError('PYTHON_LINK_GATE=FAIL')
        exe=out/'q042_native_nan_probe_v25';cmd=['gcc','-O2','-fopenmp','-rdynamic']
        for sub in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):cmd+=['-I',str(root/sub)]
        cmd += [str(HERE/'q042_class_nan_probe_v25.c'),str(binary),'-L'+libdir,'-l'+ldlib.removeprefix('lib').split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        with (out/'compile.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=c['compile_seconds'])
        p.point_ini(c,out/'point.ini');env=dict(os.environ,Q042_TRACE_DIR=str(out))
        with (out/'native.log').open('w') as log:subprocess.run([str(exe),str(out/'point.ini')],env=env,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=c['runtime_seconds'])
        events=[json.loads(line) for line in (out/'native_trace.jsonl').read_text().splitlines()]
        r.update(events=events,class_binary_sha256=sha(binary),class_commit=CLASS_COMMIT,source_tree_gate='PASS',binary_route=str(binary),native_executable_sha256=sha(exe),compile_command=cmd,parameters=c['parameters'],python_version=platform.python_version(),compiler_version=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0])
        r.update(summarize_trace(events,c['parameters']['tau_reio']))
        matches={n:sha(out/n)==digest for n,digest in c['unchanged_v23_raw_hashes'].items()}
        r.update(unchanged_v23_v24_raw_products=matches,native_inspection=p.inspect_tables(out))
        if not all(matches.values()):raise ValueError('OBSERVATIONAL_EQUIVALENCE_GATE=FAIL raw changed products preserved')
    except Exception as e:r.update(trace_gate='FAIL',exception_type=type(e).__name__,exception=str(e))
    r['files']={f.name:sha(f) for f in out.iterdir() if f.is_file()};r['elapsed_seconds']=time.monotonic()-start;write(out/'q042_class_nan_result_v25.json',r)
    if r['trace_gate']!='PASS':raise ValueError('UPSTREAM_OBSERVATION_GATE=FAIL record preserved; no retry')

def collect(source,out):
    c=contract();p=module('attribution_v23','q042_class_diagnostic_v23.py');records=[];errors=[]
    for f in sorted(Path(source).rglob('q042_class_nan_result_v25.json')):
        try:
            r=json.loads(f.read_text());records.append(r)
            if not r.get('files'):raise ValueError('RAW_MEMBERS_MISSING')
            for name,digest in r['files'].items():
                if Path(name).name!=name or sha(f.parent/name)!=digest:raise ValueError('RAW_MEMBER_HASH_GATE=FAIL')
            events=[json.loads(line) for line in (f.parent/'native_trace.jsonl').read_text().splitlines()];s=summarize_trace(events,c['parameters']['tau_reio'])
            if r.get('events')!=events or any(r.get(k)!=v for k,v in s.items()):raise ValueError('RAW_TRACE_RECONSTRUCTION_GATE=FAIL')
            if r.get('parameters')!=c['parameters'] or r.get('source_tree_gate')!='PASS' or r.get('compiled_core_algorithm_changed') is not False:raise ValueError('FROZEN_STATE_GATE=FAIL')
            if r.get('contract_sha256')!=sha(HERE/'q042_class_nan_contract_v25.json') or r.get('scientific_question')!=c['scientific_question'] or r.get('original_scientific_spec_sha256')!=c['original_scientific_spec_sha256']:raise ValueError('CONTRACT_LINEAGE_GATE=FAIL')
            if r.get('native_inspection')!=p.inspect_tables(f.parent):raise ValueError('TABLE_RECONSTRUCTION_GATE=FAIL')
            if any(sha(f.parent/n)!=digest for n,digest in c['unchanged_v23_raw_hashes'].items()):raise ValueError('TABLE_IDENTITY_GATE=FAIL')
        except Exception as e:errors.append(dict(file=str(f),error=str(e)))
    result=collect_records(records,os.environ.get('GITHUB_RUN_ID','LOCAL'),os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),errors);write(out,result)
    if result['technical_gate']!='PASS':raise ValueError('COMPLETENESS_GATE=FAIL record preserved')

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['static','observe','collect']);p.add_argument('--root',default='.');p.add_argument('--class-root',default='external/class_ede');p.add_argument('--out',default='diag_results');p.add_argument('--source',default='collected');a=p.parse_args()
    if a.command=='static':static(a.root)
    elif a.command=='observe':observe(a.out,a.class_root)
    else:collect(a.source,a.out)
if __name__=='__main__':main()
