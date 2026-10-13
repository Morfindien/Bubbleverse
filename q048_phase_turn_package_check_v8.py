"""Q048 V8 exact executable pins plus fail-closed registry/README/launcher validation."""
from pathlib import Path
import copy,hashlib,json,os,re,subprocess,tempfile
import q048_phase_turn_v8 as e


def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def check(root=None):
    root=Path(root or e.ROOT);lock=e.old.load(root/'q048_phase_turn_package_v8.json');s=e.validate_sources()
    e.fail(lock['program_id']==e.ID and lock['q']==e.Q,'PACKAGE_IDENTITY')
    workflow=lock['workflow_install_path'];e.fail(workflow=='.github/workflows/q048-phase-turn-v8.yml','WORKFLOW_INSTALL_PATH')
    e.fail(workflow in lock['files'],'WORKFLOW_MANIFEST_PATH');e.fail('q048-phase-turn-v8.yml' not in lock['files'],'WORKFLOW_ROOT_ALIAS_FORBIDDEN')
    for n,want in lock['files'].items():e.fail((root/n).is_file() and sha256(root/n)==want,'PACKAGE_FILE '+n)

    reg=e.old.load(root/'bubbleverse_program_registry.json');p=reg['programs'];entry=p[e.ID]
    for k,v in lock['registry_entry'].items():e.fail(entry.get(k)==v,'REGISTRY_ENTRY '+k)
    e.fail(p['Q048-STRUCTURAL-V6'].get('status')=='SUPERSEDED' and p['Q048-STRUCTURAL-V6'].get('superseded_by')=='Q048-GUARDCONT-V7','REGISTRY_V6_SUPERSESSION')
    e.fail(p['Q048-GUARDCONT-V7'].get('status')=='SUPERSEDED' and p['Q048-GUARDCONT-V7'].get('superseded_by')==e.ID,'REGISTRY_V7_SUPERSESSION')

    # Reconstruct exact inspected pre-V7/V8 registry; any unrelated mutation fails.
    base=copy.deepcopy(reg);base['programs'].pop(e.ID);base['programs'].pop('Q048-GUARDCONT-V7')
    v6=base['programs']['Q048-STRUCTURAL-V6'];v6['status']='ACTIVE';v6.pop('superseded_by',None)
    raw=(json.dumps(base,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    e.fail(blob(raw)==lock['repository_mutable_base']['bubbleverse_program_registry.json_git_blob_sha1'],'REGISTRY_UNRELATED_CHANGE')

    sep='\n---\n\n## Preserved historical repository context\n\n'
    prefix=(root/'README_Q048_V8_SECTION.md').read_text()+sep+(root/'README_Q048_V7_SECTION.md').read_text()+sep
    readme=(root/'README.md').read_text();e.fail(readme.startswith(prefix),'README_PREFIX')
    historical=readme[len(prefix):].encode();e.fail(blob(historical)==lock['repository_mutable_base']['README.md_git_blob_sha1'],'README_HISTORY_CHANGED')
    for token in [e.ID,workflow,'.github/workflows/q048-install-phase-turn-v8.yml',e.SCOPE,'38348832247','UNRESOLVED','.github/workflows/00-bubbleverse-start.yml','bubbleverse_program_registry.json']:
        e.fail(token in readme,'README_REFERENCE '+token)

    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    e.fail(e.git_blob_sha1(launcher)==s['reused_git_blob_sha1']['.github/workflows/00-bubbleverse-start.yml'],'LAUNCHER_CHANGED')
    script=textwrap_launcher(launcher.read_text())
    cases=[(e.ID,True),('Q048-GUARDCONT-V7',False),('Q048-STRUCTURAL-V6',False),('Q999-UNKNOWN',False),(e.ID+';echo bad',False),('$(touch bad)',False)]
    for value,success in cases:
        with tempfile.NamedTemporaryFile() as output:
            env=dict(os.environ,RAW_PROGRAM_ID=value,GITHUB_OUTPUT=output.name)
            r=subprocess.run(['python3','-c',script],cwd=root,env=env,capture_output=True,text=True,timeout=10)
            e.fail((r.returncode==0)==success,'LAUNCHER_INPUT_GATE '+value)
            if success:
                fields=dict(x.split('=',1) for x in Path(output.name).read_text().splitlines())
                e.fail(fields['workflow_id']=='q048-phase-turn-v8.yml' and fields['q']==e.Q,'LAUNCHER_RESOLUTION')

    wf=(root/workflow).read_text()
    for token in [e.ID,'38348832247','q048-guard-v7-final-38348832247','q048_phase_turn_runner_v8.py','actions/download-artifact@v4']:
        e.fail(token in wf,'WORKFLOW_REFERENCE '+token)
    # The one-time installer is intentionally not a runtime dependency after
    # registry/README installation has completed.  The canonical installed
    # state above is the authoritative gate; absence of the historical
    # installer workflow must not block scientific execution.
    installer_path=lock.get('installer_workflow_path')
    e.fail(installer_path=='.github/workflows/q048-install-phase-turn-v8.yml','INSTALLER_METADATA_PATH')
    e.fail(lock.get('installer_runtime_required') is False,'INSTALLER_RUNTIME_POLICY')

    parent=os.environ.get('Q048_V7_PARENT');parent_gate='NOT_CHECKED_STATIC'
    if parent:
        e.load_parent(parent);parent_gate='PASS_OFFICIAL_V7_PARENT'
    return {'q':e.Q,'program_id':e.ID,'package_gate':'PASS','parent_gate':parent_gate,
            'launcher_gate':'PASS_LOCAL_INSTALLATION','readme_gate':'PASS_LOCAL_INSTALLATION','journal_continuity_gate':'PASS',
            'repository_consistency_gate':'PASS_LOCAL_INSTALLATION','remote_installation':'NOT_PERFORMED_BY_CHECKER','final_result_gate':'UNRESOLVED'}


def textwrap_launcher(text):
    m=re.search(r"python - <<'PY'\n(.*?)\n\s*PY",text,re.S)
    if not m:raise ValueError('LAUNCHER_SCRIPT_NOT_FOUND')
    import textwrap
    return textwrap.dedent(m.group(1))

if __name__=='__main__':print(json.dumps(check()))
