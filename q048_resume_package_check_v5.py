"""Pin executable files, retain source/input history and exercise safe launcher."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile
import q048_resume_v5 as e

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def check(root=None):
    root=Path(root or e.ROOT);lock=e.load(root/'q048_resume_package_v5.json')
    if lock.get('q')!=e.Q or lock.get('program_id')!=e.ID or lock.get('version')!=e.VERSION:raise ValueError('PACKAGE_IDENTITY')
    for name,want in lock['files'].items():
        p=root/name
        if not p.is_file() or sha(p.read_bytes())!=want:raise ValueError('PACKAGE_FILE '+name)
    for name,want in lock['reused_source_sha256'].items():
        if sha((root/name).read_bytes())!=want:raise ValueError('PINNED_BACKEND '+name)
    settings=e.load(root/'q048_resume_config_v5.json');e.validate_settings(settings)
    if settings['source_config_sha256']!=sha((root/settings['source_config_file']).read_bytes()):raise ValueError('SOURCE_CONFIG_HASH')
    cfg=e.p.validate_config(e.load(root/settings['source_config_file']))
    for case in e.p.CASES:e.parent_from_asset(case,settings)
    registry=e.load(root/'bubbleverse_program_registry.json')['programs'];entry=registry[e.ID]
    protected={k:v for k,v in registry.items() if k not in (e.ID,'Q048-RESUME-V4')}
    if len(protected)!=lock['protected_registry_count'] or sha(canonical(protected))!=lock['protected_registry_sha256']:
        raise ValueError('REGISTRY_HISTORY')
    legacy=dict(registry['Q048-RESUME-V4'])
    if legacy.pop('superseded_by',None)!=e.ID or legacy.get('status')!='SUPERSEDED':raise ValueError('LEGACY_ROUTING')
    legacy['status']='ACTIVE'
    if sha(canonical(legacy))!=lock['original_v4_entry_sha256']:raise ValueError('LEGACY_ENTRY_REWRITTEN')
    target='.github/workflows/q048-resume-v5.yml'
    for k,want in {'q':e.Q,'status':'ACTIVE','version':'v5','program_version':'v5','workflow_version':'v5',
                   'workflow_path':target,'workflow_id':'q048-resume-v5.yml','scientific_program':'q048_resume_v5.py',
                   'config':'q048_resume_config_v5.json','scientific_acceptance':False}.items():
        if entry.get(k)!=want:raise ValueError('REGISTRY_TARGET '+k)
    readme=(root/'README.md').read_text();workflow=(root/target).read_text()
    for token in (e.ID,target,'CONDITIONAL_SOURCE_REAL_PREFIX','UNRESOLVED',
                  '.github/workflows/00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if token not in readme:raise ValueError('README_PATH_OR_SCOPE '+token)
    if e.ID not in workflow or 'timeout-minutes: 50' not in workflow:raise ValueError('WORKFLOW_TARGET')
    for n in lock['install_files']:
        if not (root/n).is_file():raise ValueError('INSTALL_FILE_MISSING '+n)
    tail=lock['journal_tail'];journal=(root/'Q047_SAMLET_JOURNAL.md').read_bytes()
    if len(journal)<tail['bytes'] or sha(journal[-tail['bytes']:])!=tail['sha256']:raise ValueError('JOURNAL_HISTORY')
    if cfg['scientific_question'].encode() not in journal:raise ValueError('JOURNAL_QUESTION_LOST')
    # Execute the existing launcher's resolver without any dispatch/network call.
    launcher=(root/'.github/workflows/00-bubbleverse-start.yml').read_text()
    match=re.search(r"python - <<'PY'\n(.*?)\n\s*PY",launcher,re.S)
    if not match:raise ValueError('LAUNCHER_RESOLVER_MISSING')
    import textwrap
    script=textwrap.dedent(match.group(1))
    for value,success in [(e.ID,True),('Q048-RESUME-V4',False),('Q999-UNKNOWN',False),
                          ('Q048-RESUME-V5;echo bad',False),('$(touch bad)',False),('Q048-RESUME-V5\nfoo',False)]:
        with tempfile.NamedTemporaryFile() as out:
            env=dict(os.environ,RAW_PROGRAM_ID=value,GITHUB_OUTPUT=out.name)
            proc=subprocess.run(['python3','-c',script],cwd=root,env=env,capture_output=True,text=True,timeout=10)
            if (proc.returncode==0)!=success:raise ValueError('LAUNCHER_INPUT_GATE')
            if success:
                fields=dict(line.split('=',1) for line in Path(out.name).read_text().splitlines())
                if fields.get('workflow_id')!='q048-resume-v5.yml' or fields.get('q')!=e.Q:raise ValueError('LAUNCHER_RESOLUTION')
    return {'q':e.Q,'program_id':e.ID,'package_gate':'PASS','q_identity_gate':'PASS',
            'journal_continuity_gate':'PASS','source_pin_gate':'PASS','launcher_gate':'PASS_LOCAL_INSTALLATION',
            'readme_gate':'PASS_LOCAL_INSTALLATION','repository_consistency_gate':'PASS_LOCAL_INSTALLATION',
            'remote_installation':'OBSERVED_CURRENT_ACTIONS_JOB' if os.environ.get('GITHUB_ACTIONS')=='true' else 'NOT_PERFORMED',
            'registration_evidence':'ENTRY_PRESENT_IN_CHECKED_SNAPSHOT','final_result_gate':'UNRESOLVED'}

if __name__=='__main__':print(json.dumps(check()))
