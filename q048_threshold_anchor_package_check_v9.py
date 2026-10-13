"""Q048 V9 exact package pins plus fail-closed registry/README/launcher validation."""
from pathlib import Path
import copy, hashlib, json, subprocess

import q048_threshold_anchor_v9 as e


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def check(root=None):
    root=Path(root or e.ROOT)
    lock=e.old.load(root/'q048_threshold_anchor_package_v9.json')
    s=e.validate_sources()
    e.fail(lock['schema']=='Q048_THRESHOLD_ANCHOR_PACKAGE_V9','PACKAGE_SCHEMA')
    e.fail(lock['program_id']==e.ID and lock['q']==e.Q and lock['version']==e.VERSION,'PACKAGE_IDENTITY')

    workflow=lock['workflow_install_path']
    e.fail(workflow=='.github/workflows/q048-threshold-anchor-v9.yml','WORKFLOW_INSTALL_PATH')
    e.fail(workflow in lock['files'],'WORKFLOW_MANIFEST_PATH')
    e.fail('q048-threshold-anchor-v9.yml' not in lock['files'],'WORKFLOW_ROOT_ALIAS_FORBIDDEN')

    installer=lock.get('installer_workflow_path')
    e.fail(installer=='.github/workflows/q048-install-threshold-v9.yml','INSTALLER_METADATA_PATH')
    e.fail(lock.get('installer_runtime_required') is False,'INSTALLER_RUNTIME_POLICY')
    e.fail(installer not in lock['files'],'INSTALLER_MUST_NOT_BE_RUNTIME_FILE')

    for name,want in lock['files'].items():
        p=root/name
        e.fail(p.is_file() and sha256(p)==want,'PACKAGE_FILE '+name)

    reg=e.old.load(root/'bubbleverse_program_registry.json')
    programs=reg['programs']
    e.fail(e.ID in programs and 'Q048-PHASETURN-V8' in programs,'REGISTRY_ENTRIES')
    entry=programs[e.ID]
    for k,v in lock['registry_entry'].items():
        e.fail(entry.get(k)==v,'REGISTRY_ENTRY '+k)
    e.fail(entry['status']=='ACTIVE' and entry.get('supersedes')=='Q048-PHASETURN-V8','REGISTRY_V9_ACTIVE')
    v8=programs['Q048-PHASETURN-V8']
    e.fail(v8.get('status')=='SUPERSEDED' and v8.get('superseded_by')==e.ID,'REGISTRY_V8_SUPERSESSION')

    # Reconstruct the exact inspected V8 canonical registry.  Any unrelated
    # mutation is rejected rather than silently absorbed into this package.
    base=copy.deepcopy(reg)
    base['programs'].pop(e.ID)
    oldv8=base['programs']['Q048-PHASETURN-V8']
    oldv8['status']='ACTIVE';oldv8.pop('superseded_by',None)
    raw=(json.dumps(base,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    e.fail(blob(raw)==lock['repository_mutable_base']['bubbleverse_program_registry.json_git_blob_sha1'],
           'REGISTRY_UNRELATED_CHANGE')

    sep='\n---\n\n## Preserved historical repository context\n\n'
    prefix=(root/'README_Q048_V9_SECTION.md').read_text()+sep
    readme=(root/'README.md').read_text()
    e.fail(readme.startswith(prefix),'README_PREFIX')
    historical=readme[len(prefix):].encode()
    e.fail(blob(historical)==lock['repository_mutable_base']['README.md_git_blob_sha1'],
           'README_HISTORY_CHANGED')
    for token in [e.ID,workflow,e.SCOPE,'38361759433','Mathematics-009',
                  'UNRESOLVED','NOT_COMPUTED','RESULT INGESTION & ROUTING ENGINE']:
        e.fail(token in readme,'README_TOKEN '+token)

    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    e.fail(e.git_blob_sha1(launcher)==s['reused_git_blob_sha1']['.github/workflows/00-bubbleverse-start.yml'],
           'LAUNCHER_BLOB')
    ltxt=launcher.read_text()
    for token in ['🚀 BUBBLEVERSE START','PROGRAM_ID_GATE=FAIL',"status != 'ACTIVE'",
                  'gh workflow run','$WORKFLOW_ID']:
        e.fail(token in ltxt,'LAUNCHER_TOKEN '+token)

    wtxt=(root/workflow).read_text()
    for token in [e.ID,'38293480870','38348832247','38361759433',
                  'q048-structural-v6-final-38293480870',
                  'q048-guard-v7-final-38348832247',
                  'q048-phase-turn-v8-final-38361759433',
                  'q048_v9_repository_patch.py --verify-only',
                  'q048_threshold_anchor_tests_v9',
                  'q048_threshold_anchor_runner_v9.py',
                  'q048_threshold_anchor_final_v9.json']:
        e.fail(token in wtxt,'WORKFLOW_TOKEN '+token)

    for key in ('parent_v6','parent_v7','parent_v8'):
        e.fail(lock[key]==s[key],'PARENT_LOCK '+key)

    # Redundant installed-state verifier; it must not write in normal runtime.
    subprocess.run(['python',str(root/'q048_v9_repository_patch.py'),'--verify-only'],
                   cwd=root,check=True)
    print('Q048_THRESHOLD_V9_PACKAGE_GATE=PASS')
    return {'gate':'PASS','runtime_file_count':len(lock['files'])}


if __name__=='__main__':
    check()
