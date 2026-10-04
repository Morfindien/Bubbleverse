#!/usr/bin/env python3
"""Install the one diagnostic registry entry and differential README update.

Run locally after copying files. This helper never commits or dispatches.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

PROGRAM_ID='Q042-STOCKDIAG-V20'
TARGET='q042-stock-diagnostic-v20.yml'
ENTRY={
 'q':'Q-042','status':'ACTIVE','workflow_id':TARGET,'target_ref':'main',
 'program_version':'20','workflow_version':'20',
 'scientific_task':'One stock-resume diagnostic and one exact CLASS failure-point replay; no production restart',
 'config':'q042_stock_diagnostic_contract_v20.json',
 'scientific_spec':'q042_production_spec_v1.json',
 'source_execution_commit':'d0f92c7f2ce53da32818244f8847f8e745e20c4f',
 'result_artifacts':['q042-v20-<RUN_ID>-diagnostic-final'],
 'science_status':'UNRESOLVED','supersedes':None,
}
OLD='''It verifies, among other things:

- the `PROGRAM_ID` exists
- the program is active
- the Q identity is valid
- the target workflow is valid
- the expected result-artifact contract is defined

The launcher then dispatches the registered workflow and tracks the child execution.'''
NEW='''It verifies the exact `PROGRAM_ID`, active status, Q identity and allowed workflow/ref syntax against `bubbleverse_program_registry.json`.

The permanent launcher is `.github/workflows/00-bubbleverse-start.yml`. It dispatches the registered target; that target validates its inputs and publishes its own results. Open the child run to inspect its outcome.

### Q-042 bounded execution diagnosis

`Q042-STOCKDIAG-V20` runs one isolated CamSpec/EDE/FULL stock resume (at most 240 minutes) and one exact CLASS error-point replay (at most 15 minutes). It preserves the V18 state, records in-memory versus durable progress and stops after the diagnostic. It does not restart the 20-cell production matrix, recompute BOBYQA, or provide a validated cosmological result.

After installation: **🚀 BUBBLEVERSE START → Q042-STOCKDIAG-V20 → Run workflow**. Return the diagnostic-final JSON, both diagnostic artifacts and `q042_execution_handoff_v20.md` to the Result Ingestion & Routing Engine. Q-042 remains `UNRESOLVED` until its frozen scientific gates pass.'''

def readme_update(text):
    if NEW in text:
        if '000 🚀 BUBBLEVERSE START — SEGMENTED V5' in text:raise ValueError('README_MIXED_STATE_GATE=FAIL')
        return text
    if text.count(OLD)!=1 or text.count('000 🚀 BUBBLEVERSE START — SEGMENTED V5')!=1:
        raise ValueError('README_DIFFERENTIAL_ANCHOR_GATE=FAIL')
    return text.replace(OLD,NEW).replace('000 🚀 BUBBLEVERSE START — SEGMENTED V5','🚀 BUBBLEVERSE START')

def registry_update(data):
    programs=data['programs'];previous=programs.get(PROGRAM_ID)
    if previous is not None and previous!=ENTRY:raise ValueError('REGISTRY_ENTRY_CONFLICT_GATE=FAIL')
    programs[PROGRAM_ID]=ENTRY
    return data

def check_package(root):
    manifest=json.loads((root/'q042_stock_diagnostic_manifest_v20.json').read_text())
    if manifest['q']!='Q-042' or manifest['program_id']!=PROGRAM_ID:raise ValueError('PACKAGE_IDENTITY_GATE=FAIL')
    for name,digest in manifest['files'].items():
        path=root/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('PACKAGE_HASH_GATE=FAIL '+name)
    c=json.loads((root/'q042_stock_diagnostic_contract_v20.json').read_text())
    if c['program_id']!=PROGRAM_ID or c['probe_seconds']!=14400 or c['class_seconds']!=900:
        raise ValueError('PACKAGE_CONTRACT_GATE=FAIL')
    return manifest

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();root=Path.cwd()
    check_package(root)
    target=root/'.github/workflows'/TARGET
    if not target.is_file():raise ValueError('TARGET_WORKFLOW_GATE=FAIL')
    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    if not launcher.is_file() or 'name: "🚀 BUBBLEVERSE START"' not in launcher.read_text():raise ValueError('PERMANENT_LAUNCHER_GATE=FAIL')
    registry=root/'bubbleverse_program_registry.json';readme=root/'README.md'
    old_r=registry.read_bytes();old_m=readme.read_bytes()
    d=registry_update(json.loads(old_r));m=readme_update(old_m.decode())
    if a.check:
        if json.loads(old_r)['programs'].get(PROGRAM_ID)!=ENTRY or m.encode()!=old_m:
            raise ValueError('LIVE_INSTALL_GATE=FAIL apply helper first')
        print('Q042_STOCKDIAG_PACKAGE_REGISTRY_README_GATE=PASS');return
    new_r=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode();new_m=m.encode()
    try:
        registry.write_bytes(new_r);readme.write_bytes(new_m)
    except BaseException:
        registry.write_bytes(old_r);readme.write_bytes(old_m);raise
    print('Q042_STOCKDIAG_REGISTRY_GATE=PASS')
    print('Q042_STOCKDIAG_README_GATE=PASS')
    print('NO_COMMIT_NO_DISPATCH')

if __name__=='__main__':main()
