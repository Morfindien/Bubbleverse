"""Q048 verified prefix continuation. Frozen physics; independent work budgets.

Every carried source-real cell is reverified before continuation. Native hints
and stored PASS flags are not initial-error certificates. Scope stays CONDITIONAL.
Legacy V1 boxes are reconstructed from its pinned exact generation rule.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json,os,platform,sys,time
import q048_prefix_v1 as p

ID='Q048-RESUME-V3';VERSION='v3';ROOT=Path(__file__).resolve().parent
Q=p.Q;SOURCE=p.SOURCE

def load(path):
    b=Path(path).read_bytes()
    if len(b)>32_000_000:raise ValueError('CHECKPOINT_SIZE_CAP')
    return json.loads(b,object_pairs_hook=p.old.unique,
        parse_constant=lambda x:(_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def objhash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def coordinate(value):
    # Continuation extends exact dyadic denominators beyond V1's 1000-character
    # input cap. Only this coordinate parser changes; no proof value is rounded.
    if isinstance(value,str):
        if len(value)>4096:raise ValueError('COORDINATE_SIZE_CAP')
        value=F(value)
    return p.old.rational(value)

def legacy_box(current,predictor):
    box=[]
    for i,y in enumerate(current):
        center=(y.lo+y.hi)/2;step=abs(p.exact(predictor[i][1]));err=(y.hi-y.lo)/2
        pad=max(F('1e-9') if i==0 else F('1e-15'),err*2,step*2)
        box.append([str(center-pad-step),str(center+pad+step)])
    return box

def verify_background_cell(cell,now,current,t):
    a0=coordinate(cell['a0']);a1=coordinate(cell['a1'])
    if a0!=now or a1<=a0 or a1>F(1,2871):raise ValueError('BACKGROUND_PARTITION')
    width=a1-a0
    field=lambda xi,y:[v*width/(a0+width*xi) for v in p.pre.ede_field(a0+width*xi,y,t)[0]]
    box=cell.get('box',legacy_box(current,cell['predictor']))
    candidate={'t0':'0','t1':'1','predictor':cell['predictor'],'box':box}
    report=p.certify(candidate,current,field)
    if report!=cell['certificate'] or not report['closed']:raise ValueError('BACKGROUND_CERTIFICATE_MISMATCH')
    state=[p.old.interval(v) for v in report['whole_state']]
    bg=p.pre.background(p.m.I(a0,a1),t,state)
    forcing={k:p.pairs(v) for k,v in bg.items()}
    if bg['ede_latch'].hi>=F(1,2) or forcing!=cell['forcing']:raise ValueError('BACKGROUND_FORCING_OR_SOURCE_GUARD')
    return a1,[p.old.interval(v) for v in report['endpoint']]

def cursor(bg):return coordinate(bg['certified_end_a']),[p.old.interval(x) for x in bg['endpoint']]

def background_at(a,t,bg,cell=None):
    if t['ede'] is None:return p.pre.background(a,t)
    if cell is None:raise ValueError('VERIFIED_BACKGROUND_CELL_REQUIRED')
    return p.pre.background(a,t,[p.old.interval(v) for v in cell['certificate']['whole_state']])

def verify_thermal(row,t,bg,thermal,deadline):
    now=1/(1-p.point(row['thermal_starts'][0]['mz']).lo);current=[p.m.I(0)]
    boundaries=[1/(1-p.point(s['mz']).lo) for s in row['thermal_starts'][1:5]]
    for cell in thermal['cells']:
        if time.monotonic()>=deadline:raise ValueError('CHECKPOINT_VERIFY_WORK_CAP')
        a0=coordinate(cell['a0']);a1=coordinate(cell['a1'])
        j=sum(a0>=v for v in boundaries)
        if a0!=now or a1<=a0 or j>=4 or a1>boundaries[j] or cell['mode']!=p.pre.MODES[j]:raise ValueError('THERMAL_PARTITION_MODE')
        covered=None
        if t['ede'] is not None:
            hits=[b for b in bg['cells'] if F(b['a0'])<=a0 and F(b['a1'])>=a1]
            if len(hits)!=1:raise ValueError('THERMAL_BACKGROUND_COVERAGE')
            covered=hits[0]
        width=a1-a0;getbg=lambda a:background_at(a,t,bg,covered)
        field=lambda xi,y:[p.pre.thermal(cell['mode'],a0+width*xi,y[0],t,getbg(a0+width*xi))['rate']*width/(a0+width*xi)]
        candidate={'t0':'0','t1':'1','predictor':cell['predictor'],'box':cell.get('box',[['-1/1000000','1/50']])}
        report=p.certify(candidate,current,field)
        if report!=cell['certificate'] or not report['closed']:raise ValueError('THERMAL_CERTIFICATE_MISMATCH')
        info=p.pre.thermal(cell['mode'],p.m.I(a0,a1),p.old.interval(report['whole_state'][0]),t,getbg(p.m.I(a0,a1)))
        if p.pairs(info['Tmat'])!=cell['Tmat_K'] or p.pairs(info['x'])!=cell['xe_thermal']:raise ValueError('THERMAL_OUTPUT_MISMATCH')
        now=a1;current=[p.old.interval(report['endpoint'][0])]
    if thermal.get('certified_end_a') is not None and F(thermal['certified_end_a'])!=now:raise ValueError('THERMAL_CURSOR')
    if thermal.get('endpoint') is not None and thermal['endpoint']!=list(map(p.pairs,current)):raise ValueError('THERMAL_ENDPOINT')
    if now==F(1,2871):
        if thermal.get('onset_w')!=p.pairs(current[0]) or thermal.get('onset_q')!=p.pairs(p.pre.onset(current[0],p.m.I(now),t)):raise ValueError('ONSET_CERTIFICATE_MISMATCH')
    return now,current

def verify_record(record,row,t,seconds):
    start=time.monotonic();deadline=start+seconds
    if (record.get('q_assignment')!='PROPOSED_UNVERIFIED' or record.get('case_id')!='NOT_ASSIGNED'
        or record.get('scope')!=p.FINAL_SCOPE or record.get('actual_source_admission')!='UNRESOLVED'
        or hashlib.sha256(record.get('scientific_question','').encode()).hexdigest()!='c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436'):
        raise ValueError('CHECKPOINT_SCIENTIFIC_IDENTITY')
    if record.get('q')!=Q or record.get('source_commit')!=SOURCE or record.get('configuration')!=row['background']['case']:raise ValueError('CHECKPOINT_Q_SOURCE_CASE')
    if record.get('source_input_hashes')!=row['source_input_hashes'] or record.get('final_result_gate')!='UNRESOLVED':raise ValueError('CHECKPOINT_INPUT_OR_SCOPE')
    initial,a,state=p.source_initial(row,t)
    if initial!=record['source_initialization'] or initial['initial_conditions_gate']!='PASS_CONDITIONAL':raise ValueError('CHECKPOINT_INITIAL_SOURCE_BRANCH')
    bg=record['background'];now=a.lo
    if t['ede'] is not None:
        for cell in bg['cells']:
            if time.monotonic()>=deadline:raise ValueError('CHECKPOINT_VERIFY_WORK_CAP')
            now,state=verify_background_cell(cell,now,state,t)
        if str(now)!=bg['certified_end_a'] or list(map(p.pairs,state))!=bg['endpoint']:raise ValueError('BACKGROUND_CURSOR')
    else:
        if bg['cells'] or bg['certified_end_a']!='1/2871':raise ValueError('LCDM_BACKGROUND_REFERENCE')
        if p.pre.background(p.m.I(a.lo,F(1,2871)),t)['H'].lo<=0:raise ValueError('LCDM_BACKGROUND_POSITIVITY')
    thermal_cursor=verify_thermal(row,t,bg,record['thermal'],deadline)
    if time.monotonic()>deadline:raise ValueError('CHECKPOINT_VERIFY_WORK_CAP')
    return {'gate':'PASS_CONDITIONAL_RECOMPUTED','background_cells':len(bg['cells']),
            'thermal_cells':len(record['thermal']['cells']),'elapsed_seconds':time.monotonic()-start},thermal_cursor

def continue_background(record,t,settings,save):
    bg=record['background']
    if t['ede'] is None or F(bg['certified_end_a'])==F(1,2871):return
    now,current=cursor(bg);start=now;deadline=time.monotonic()+settings['background_seconds'];new=0;reason='NEW_CELL_CAP'
    while now<F(1,2871) and new<settings['max_new_cells_per_stage'] and time.monotonic()<deadline:
        a1=min(F(1,2871),now*F(5,4));accepted=None;center=[(v.lo+v.hi)/2 for v in current]
        for _ in range(settings['max_halvings']+1):
            if time.monotonic()>=deadline:reason='BACKGROUND_WALL_TIME_CAP';break
            if len(str(a1))>4096:reason='COORDINATE_SIZE_CAP';break
            width=a1-now;field=lambda xi,y:[v*width/(now+width*xi) for v in p.pre.ede_field(now+width*xi,y,t)[0]]
            try:
                slopes=list(map(p.pre.value,field(p.m.I(0),[p.m.A(c) for c in center])))
                pred=[[str(center[i]),str((slopes[i].lo+slopes[i].hi)/2)] for i in range(2)]
                box=legacy_box(current,pred);candidate={'t0':'0','t1':'1','predictor':pred,'box':box}
                proof=p.certify(candidate,current,field)
                if proof['closed']:
                    forcing=p.pre.background(p.m.I(now,a1),t,[p.old.interval(v) for v in proof['whole_state']])
                    if forcing['ede_latch'].hi<F(1,2):
                        accepted={'a0':str(now),'a1':str(a1),'predictor':pred,'box':box,'certificate':proof,'forcing':{k:p.pairs(v) for k,v in forcing.items()}};break
                    reason='SOURCE_GUARD_NOT_SEPARATED'
                else:reason='BACKGROUND_TUBE_NOT_CLOSED'
            except (ValueError,AssertionError,ZeroDivisionError) as e:reason=type(e).__name__+':'+str(e)
            a1=(now+a1)/2
        if accepted is None:break
        bg['cells'].append(accepted);now=a1;current=[p.old.interval(v) for v in proof['endpoint']];new+=1
        bg.update(certified_end_a=str(now),endpoint=list(map(p.pairs,current)))
        if new%settings['checkpoint_every_cells']==0:save('BACKGROUND_PROGRESS')
    if time.monotonic()>=deadline and now<F(1,2871):reason='BACKGROUND_WALL_TIME_CAP'
    bg.update(status='COMPLETE' if now==F(1,2871) else 'PARTIAL',blocker=None if now==F(1,2871) else reason)
    record['background_continuation']={'start_a':str(start),'end_a':str(now),'new_cells':new,'budget_seconds':settings['background_seconds']}
    save('BACKGROUND_STAGE_DONE')

def continue_thermal(record,row,t,settings,start_cursor,save):
    bg=record['background'];th=record['thermal'];now,current=start_cursor;start=now
    end=F(1,2871);available=min(end,F(bg['certified_end_a']))
    if now==end:return
    if available<=now:
        th.update(status='PARTIAL',blocker='BACKGROUND_COVERAGE_REQUIRED');return
    boundaries=[1/(1-p.point(s['mz']).lo) for s in row['thermal_starts'][1:5]]
    deadline=time.monotonic()+settings['thermal_seconds'];new=0;reason='NEW_CELL_CAP'
    while now<available and new<settings['max_new_cells_per_stage'] and time.monotonic()<deadline:
        j=sum(now>=v for v in boundaries);mode=p.pre.MODES[j];a1=min(boundaries[j],now*F(5,4),available)
        covered=None
        if t['ede'] is not None:
            hits=[b for b in bg['cells'] if F(b['a0'])<=now<F(b['a1'])]
            if len(hits)!=1:reason='VERIFIED_BACKGROUND_COVERAGE_REQUIRED';break
            covered=hits[0];a1=min(a1,F(covered['a1']))
        getbg=lambda a:background_at(a,t,bg,covered);accepted=None
        for _ in range(settings['max_halvings']+1):
            if time.monotonic()>=deadline:reason='THERMAL_WALL_TIME_CAP';break
            width=a1-now;mid=now+width/2
            field=lambda xi,y:[p.pre.thermal(mode,now+width*xi,y[0],t,getbg(now+width*xi))['rate']*width/(now+width*xi)]
            try:
                center=(current[0].lo+current[0].hi)/2 if mode=='brec' else (1/(1+p.pre.thermal(mode,p.m.I(mid),p.m.I(0),t,getbg(p.m.I(mid)))['beta'])).lo
                box=[['-1/1000000','1/50']];pred=[[str(center)]]
                proof=p.certify({'t0':'0','t1':'1','predictor':pred,'box':box},current,field)
                if proof['closed']:
                    info=p.pre.thermal(mode,p.m.I(now,a1),p.old.interval(proof['whole_state'][0]),t,getbg(p.m.I(now,a1)))
                    accepted={'a0':str(now),'a1':str(a1),'mode':mode,'predictor':pred,'box':box,'certificate':proof,'Tmat_K':p.pairs(info['Tmat']),'xe_thermal':p.pairs(info['x'])};break
                reason='THERMAL_TUBE_NOT_CLOSED'
            except (ValueError,AssertionError,ZeroDivisionError) as e:reason=type(e).__name__+':'+str(e)
            a1=(now+a1)/2
        if accepted is None:break
        th['cells'].append(accepted);now=a1;current=[p.old.interval(proof['endpoint'][0])];new+=1
        th.update(certified_end_a=str(now),endpoint=list(map(p.pairs,current)))
        if new%settings['checkpoint_every_cells']==0:save('THERMAL_PROGRESS')
    if time.monotonic()>=deadline and now<available:reason='THERMAL_WALL_TIME_CAP'
    if now==available and available<end:reason='BACKGROUND_COVERAGE_REQUIRED'
    full=now==end;th.update(status='COMPLETE' if full else 'PARTIAL',blocker=None if full else reason,
        onset_w=p.pairs(current[0]) if full else None,onset_q=p.pairs(p.pre.onset(current[0],p.m.I(end),t)) if full else None)
    record['thermal_continuation']={'start_a':str(start),'end_a':str(now),'new_cells':new,'budget_seconds':settings['thermal_seconds']}
    save('THERMAL_STAGE_DONE')

def validate_settings(settings):
    if (settings.get('schema')!='Q048_RESUME_CONFIG_V3' or settings.get('version')!='v3'
        or settings.get('q_assignment')!='PROPOSED_UNVERIFIED' or settings.get('case_id')!='NOT_ASSIGNED'
        or settings.get('scope')!=p.FINAL_SCOPE or settings.get('scientific_result_gate')!='UNRESOLVED'):
        raise ValueError('CONTROL_SCOPE')
    if settings['verification_seconds']!=900:raise ValueError('VERIFICATION_SCHEDULE')
    for k in ('background_seconds','thermal_seconds'):
        if not 1<=settings[k]<=180:raise ValueError('WORK_CAP')
    if (not 1<=settings['max_new_cells_per_stage']<=64 or settings['max_halvings']!=11
        or settings['checkpoint_every_cells']!=8):raise ValueError('CELL_SETTINGS')

def proof_binding(record):
    # Bind the rechecked mathematical payload, excluding elapsed time/report metadata.
    keys=('q','scientific_question','q_assignment','case_id','scope','source_commit',
          'source_input_hashes','configuration','source_initialization','background','thermal')
    return objhash({k:record[k] for k in keys})

def parent_from_asset(case,settings):
    path=ROOT/settings['parent_file']
    if digest(path)!=settings['parent_file_sha256']:raise ValueError('PARENT_FILE_HASH')
    raw=load(path)
    if (raw.get('schema')!='Q048_RESUME_FINAL_V2' or raw.get('q')!=Q or raw.get('program_id')!='Q048-RESUME-V2'
        or raw.get('source_commit')!=SOURCE or set(raw['records'])!=set(p.CASES)
        or raw.get('job_completeness_gate')!='PASS' or raw.get('final_result_gate')!='UNRESOLVED'):
        raise ValueError('PARENT_RESULT_IDENTITY')
    r=raw['records'][case];m=raw['checkpoints'][case]['metadata']
    b=(json.dumps({'schema':'Q048_CHECKPOINT_V2','metadata':m,'record':r},indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    got=hashlib.sha256(b).hexdigest()
    if got!=settings['parent_checkpoints'][case] or got!=raw['checkpoints'][case]['sha256']:
        raise ValueError('PARENT_CHECKPOINT_HASH')
    if (m['q']!=Q or m['case']!=case or m['run_id']!=settings['parent_run_id']
        or m['config_hash']!=settings['parent_config_hash'] or m['source_commit']!=SOURCE
        or m['source_config_hash']!=settings['source_config_sha256']
        or m['stage']!='FINAL_CONDITIONAL_COMPONENT' or r['program_id']!='Q048-RESUME-V2'
        or m['background_end_a']!=r['background']['certified_end_a']
        or m['thermal_end_a']!=r['thermal'].get('certified_end_a')):
        raise ValueError('PARENT_METADATA')
    return copy.deepcopy(r),copy.deepcopy(m),got

def validate_checkpoint(x,case,settings):
    m=x['metadata'];r=x['record']
    if (x.get('schema')!='Q048_CHECKPOINT_V3' or m.get('q')!=Q or m.get('case')!=case
        or m.get('program_id')!=ID or m.get('version')!=VERSION or r.get('program_id')!=ID
        or m.get('source_commit')!=SOURCE or m.get('source_config_hash')!=settings['source_config_sha256']
        or m.get('config_hash')!=objhash(settings) or r.get('configuration')!=case
        or m.get('background_end_a')!=r['background']['certified_end_a']
        or m.get('thermal_end_a')!=r['thermal'].get('certified_end_a')):
        raise ValueError('CHECKPOINT_METADATA')
    root=m.get('migration_root',{})
    if (root.get('program_id')!='Q048-RESUME-V2' or root.get('run_id')!=settings['parent_run_id']
        or root.get('config_hash')!=settings['parent_config_hash']
        or root.get('checkpoint_sha256')!=settings['parent_checkpoints'][case] or root!=r.get('migration_root')):
        raise ValueError('CHECKPOINT_ROOT_LINEAGE')
    # Checkpoints from interrupted stages may continue after full recomputation.
    if m.get('stage')=='FINAL_CONDITIONAL_COMPONENT':
        if (r.get('tests_status')!='COMPLETE_CONDITIONAL' or r.get('post_verification',{}).get('gate')!='PASS_CONDITIONAL_RECOMPUTED'
            or r.get('verified_scientific_payload_sha256')!=proof_binding(r)
            or m.get('verified_scientific_payload_sha256')!=proof_binding(r)):
            raise ValueError('CHECKPOINT_POST_VERIFICATION')

def run(case,out,checkpoint=None,control=None):
    run_started=time.monotonic()
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    settings=load(control or ROOT/'q048_resume_config_v3.json')
    if settings.get('program_id')!=ID or settings.get('q')!=Q or settings.get('source_commit')!=SOURCE:raise ValueError('CONTROL_IDENTITY')
    validate_settings(settings)
    config_path=ROOT/settings['source_config_file']
    if digest(config_path)!=settings['source_config_sha256']:raise ValueError('SOURCE_CONFIG_HASH')
    config=p.validate_config(load(config_path));row=config['cases'][case];t=p.parameters(row)
    if checkpoint:
        x=load(checkpoint);validate_checkpoint(x,case,settings)
        record=copy.deepcopy(x['record']);parent=digest(checkpoint);oldmeta=x['metadata']
    else:
        record,oldmeta,parent=parent_from_asset(case,settings)
    inherited_counts={stage:len(record[stage]['cells']) for stage in ('background','thermal')}
    inherited_hashes={stage:objhash(record[stage]['cells']) for stage in ('background','thermal')}
    verification,start_cursor=verify_record(record,row,t,settings['verification_seconds'])
    record['parent_elapsed_seconds']=record.get('elapsed_seconds')
    record['parent_record_run_id']=record.get('run_id')
    record.update(program_id=ID,version=VERSION,checkpoint_verification=verification,parent_checkpoint_sha256=parent,
                  run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),executed_commit=os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'))
    record['new_native_evaluations']=0;record['likelihood_evaluations']=0
    record['migration_root']=record.get('migration_root',{'program_id':oldmeta['program_id'],
        'config_hash':oldmeta['config_hash'],'run_id':oldmeta['run_id'],'checkpoint_sha256':parent})
    record['inherited_counts']=inherited_counts;record['inherited_cells_hashes']=inherited_hashes
    record['tests_status']='PROVISIONAL'

    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    def save(stage):
        record['elapsed_seconds']=time.monotonic()-run_started
        record['python']=platform.python_version()
        record['conditional_H_entry_gate']='PASS_CONDITIONAL' if record['thermal']['status']=='COMPLETE' else 'UNRESOLVED'
        record['final_result_gate']='UNRESOLVED';record['actual_source_admission']='UNRESOLVED'
        meta={'q':Q,'case':case,'program_id':ID,'version':VERSION,'source_commit':SOURCE,'source_config_hash':settings['source_config_sha256'],'config_hash':objhash(settings),'parent_checkpoint_sha256':parent,'run_id':record['run_id'],'job_id':os.environ.get('GITHUB_JOB','LOCAL'),'stage':stage,'background_end_a':record['background']['certified_end_a'],'thermal_end_a':record['thermal'].get('certified_end_a'),'migration_root':record['migration_root'],'verified_scientific_payload_sha256':record.get('verified_scientific_payload_sha256')}
        p.old.write(out/(case+'_checkpoint_v3.json'),{'schema':'Q048_CHECKPOINT_V3','metadata':meta,'record':record})
        print(json.dumps({'case':case,'stage':stage,'background_cells':len(record['background']['cells']),'thermal_cells':len(record['thermal']['cells'])}),flush=True)
    save('VERIFIED_RESUME_START')
    continue_background(record,t,settings,save)
    continue_thermal(record,row,t,settings,start_cursor,save)
    record['first_blocker']='ACTUAL_REFERENCE_AND_FIRST_EVENT_REQUIRED' if record['thermal']['status']=='COMPLETE' else record['thermal'].get('blocker') or record['background'].get('blocker')
    for stage in inherited_counts:
        if objhash(record[stage]['cells'][:inherited_counts[stage]])!=inherited_hashes[stage]:
            raise ValueError('INHERITED_CERTIFICATE_REPLACED')
    save('RAW_CONTINUATION_DONE')
    post,_=verify_record(record,row,t,settings['verification_seconds'])
    record['post_verification']=post
    record['verified_scientific_payload_sha256']=proof_binding(record)
    record['tests_status']='COMPLETE_CONDITIONAL'
    save('FINAL_CONDITIONAL_COMPONENT')
    p.old.write(out/(case+'_resume_v3.json'),record)
    return record

def main():
    a=argparse.ArgumentParser();a.add_argument('--program-id',default=ID);a.add_argument('--case',choices=p.CASES,required=True)
    a.add_argument('--out',default='q048_resume_results');a.add_argument('--checkpoint');a.add_argument('--control')
    args=a.parse_args()
    if args.program_id!=ID:raise ValueError('PROGRAM_ID_GATE')
    run(args.case,args.out,args.checkpoint,args.control)
if __name__=='__main__':main()
