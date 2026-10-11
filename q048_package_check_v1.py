#!/usr/bin/env python3
"""Fail-fast candidate consistency; never dispatch or load CLASS."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from q048_inputcheck_v1 import ID, Q, CONTRACT_SHA, GateError, need, read, sha

HERE=Path(__file__).resolve().parent
def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def check(root):
    root=Path(root); pkg=read(root/'Q048_INPUTCHECK_PACKAGE_V1.json')
    need(os.environ.get('REQUESTED_PROGRAM_ID',ID)==ID,'PROGRAM_ID_GATE')
    need(pkg['q']==Q and pkg['program_id']==ID,'PACKAGE_CONTEXT')
    for name,digest in pkg['file_sha256'].items():
        p=root/name; need(p.is_file() and sha(p)==digest,'PACKAGE_FILE '+name)
    need(sha(root/'Q048_INPUTCHECK_CONTRACT_V1.json')==CONTRACT_SHA,'CONTRACT_HASH')
    contract=read(root/'Q048_INPUTCHECK_CONTRACT_V1.json')
    reg=read(root/'bubbleverse_program_registry.json')['programs']; entry=reg[ID]
    need(entry['q']==Q and entry['status']=='ACTIVE','REGISTRY_CONTEXT')
    need(entry['program_version']==entry['workflow_version']==entry['version']=='v1','REGISTRY_VERSIONS')
    need(entry['workflow_id']=='q048-input-check-v1.yml' and
         entry['workflow_path']=='.github/workflows/'+entry['workflow_id'],'REGISTRY_TARGET')
    old={k:reg[k] for k in pkg['preserved_registry_ids']}
    need(canonical_hash(old)==pkg['preserved_registry_entries_sha256'],'REGISTRY_PRESERVATION')
    need(entry['source_lock']=='Q048_INPUTCHECK_CONTRACT_V1.json' and
         entry['scientific_program']=='q048_inputcheck_v1.py' and entry['target_ref']=='main','REGISTRY_LINKS')
    journal=(root/'Q047_SAMLET_JOURNAL.md').read_text()
    need(contract['scientific_question'] in journal and 'Q-048' in journal and ID in journal,'JOURNAL_CONTEXT')
    readme=(root/'README.md').read_text()
    for name in [ID,entry['workflow_path'],'bubbleverse_program_registry.json',
                 '.github/workflows/00-bubbleverse-start.yml','Q047_SAMLET_JOURNAL.md']:
        need(name in readme,'README_REFERENCE '+name)
    need(sha(root/'.github/workflows/00-bubbleverse-start.yml')==pkg['unchanged_launcher_sha256'],
         'LAUNCHER_CHANGED_REASSESS_REQUIRED')
    # Execute the existing launcher's actual Python resolver, never its gh dispatch.
    launcher=(root/'.github/workflows/00-bubbleverse-start.yml').read_text()
    block=launcher.split("python - <<'PY'\n",1)[1].split('\n          PY',1)[0]
    resolver='\n'.join(line[10:] for line in block.splitlines())+'\n'
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)/'output'; env=dict(os.environ,RAW_PROGRAM_ID=ID,GITHUB_OUTPUT=str(out))
        cp=subprocess.run([sys.executable,'-c',resolver],cwd=root,env=env,capture_output=True,text=True,timeout=5)
        need(cp.returncode==0 and 'workflow_id=q048-input-check-v1.yml' in out.read_text(),
             'LAUNCHER_RESOLUTION')
        for bad in ['Q048-DOES-NOT-EXIST-V1','Q048-INPUTCHECK-V1;echo BAD','$(echo BAD)']:
            env['RAW_PROGRAM_ID']=bad
            cp=subprocess.run([sys.executable,'-c',resolver],cwd=root,env=env,capture_output=True,text=True,timeout=5)
            need(cp.returncode!=0,'LAUNCHER_UNKNOWN_OR_INJECTION')
    return {'q':Q,'program_id':ID,'package_gate':'PASS','registry_preservation_gate':'PASS',
        'launcher_gate':'PASS_LOCAL_RESOLVER','readme_gate':'PASS_LOCAL_CANDIDATE',
        'repository_consistency_gate':'PASS_LOCAL_CANDIDATE','remote_installation':'NOT_PERFORMED',
        'canonical_q_assignment':'UNVERIFIED','final_result_gate':'UNRESOLVED'}

if __name__=='__main__':
    try: print(json.dumps(check(HERE),indent=2))
    except (GateError,KeyError,ValueError,OSError,IndexError,subprocess.TimeoutExpired) as e:
        print('PACKAGE_GATE=FAIL '+str(e),file=sys.stderr); sys.exit(2)
