#!/usr/bin/env python3
"""Differential V22 installation; no commits, network writes or dispatch."""
from __future__ import annotations
import argparse, copy, hashlib, json, re
from pathlib import Path
PROGRAM_ID='Q042-DURABLE-V22';TARGET='q042-durable-v22.yml'
OLD='### Q-042 bounded execution diagnosis\n\n`Q042-STOCKDIAG-V21` repairs the V20 artifact-download directory error. It runs only the missing isolated CamSpec/EDE/FULL stock resume (at most 240 minutes), and imports the completed CLASS replay from V20 run 37195728280 after checking its exact artifact and record hashes. No CLASS replay is recomputed. V20 is retained as a historical broken execution target.\n\nThe diagnostic preserves the V18 state, records in-memory versus durable progress and stops. It does not restart the 20-cell production matrix, recompute BOBYQA, or provide a validated cosmological result.\n\nAfter installation: **🚀 BUBBLEVERSE START → Q042-STOCKDIAG-V21 → Run workflow**. Return the diagnostic-final JSON, both diagnostic artifacts and `q042_execution_handoff_v21.md` to the Result Ingestion & Routing Engine. Q-042 remains `UNRESOLVED` until its frozen scientific gates pass.\n\n'
NEW='### Q-042 bounded durability diagnosis\n\n`Q042-DURABLE-V22` saves complete serial PolyChord state after a whole iteration, without changing compression, covariance, clustering or posterior-update cadence. It first requires a compiled interrupted/resumed reference with identical likelihood trajectories, evidence and posterior weights. It then runs at most one isolated CamSpec/EDE/FULL diagnostic branch: one new state publication and one genuine resume, sharing a single 240-minute compute budget in a 330-minute job.\n\nThe old V18 stock checkpoint has no recoverable historical RNG or pending posterior stack. Its import is explicitly diagnostic; V22 does not claim to restore that lost trajectory. The preserved CLASS failure remains an independent production blocker. All 80 BOBYQA records, including two flag −3 failures, remain unchanged. No optimizer starts, CLASS replay, production fan-out or automatic continuation are performed.\n\nAfter installation: **🚀 BUBBLEVERSE START → Q042-DURABLE-V22 → Run workflow**. Return the V22 diagnostic-final artifact, durability-diagnostic artifact and `q042_execution_handoff_v22.md` to the Result Ingestion & Routing Engine. Q-042 remains `UNRESOLVED`. V21 remains historical evidence for the durability failure.\n\n'
PREVIOUS_ENTRY={'q': 'Q-042', 'status': 'ACTIVE', 'workflow_id': 'q042-stock-diagnostic-v21.yml', 'target_ref': 'main', 'program_version': '21', 'workflow_version': '21', 'scientific_task': 'Recover missing stock-resume diagnostic; import completed V20 CLASS replay without recomputation', 'config': 'q042_stock_diagnostic_contract_v21.json', 'scientific_spec': 'q042_production_spec_v1.json', 'source_execution_commit': 'd0f92c7f2ce53da32818244f8847f8e745e20c4f', 'result_artifacts': ['q042-v21-<RUN_ID>-diagnostic-final'], 'science_status': 'UNRESOLVED', 'supersedes': 'Q042-STOCKDIAG-V20', 'reused_class_run_id': 37195728280, 'reused_class_artifact_id': 11300612265}
ENTRY={'q': 'Q-042', 'status': 'ACTIVE', 'workflow_id': 'q042-durable-v22.yml', 'target_ref': 'main', 'program_version': '22', 'workflow_version': '22', 'scientific_task': 'Complete serial state checkpoint, compiled interruption reference and at most one bounded diagnostic pilot', 'config': 'q042_durable_contract_v22.json', 'scientific_spec': 'q042_production_spec_v1.json', 'source_execution_commit': 'd0f92c7f2ce53da32818244f8847f8e745e20c4f', 'result_artifacts': ['q042-v22-<RUN_ID>-diagnostic-final', 'q042-v22-<RUN_ID>-durability-diagnostic'], 'science_status': 'UNRESOLVED', 'supersedes': 'Q042-STOCKDIAG-V21', 'new_bobyqa_starts': 0, 'production_restart_authorized': False}

def readme_update(text):
    if text.count(NEW)==1 and OLD not in text:return text
    if text.count(OLD)!=1 or NEW in text:raise ValueError('README_DIFFERENTIAL_ANCHOR_GATE=FAIL')
    return text.replace(OLD,NEW,1)

def registry_update(data):
    data=copy.deepcopy(data);programs=data['programs']
    historical=dict(PREVIOUS_ENTRY,status='SUPERSEDED',superseded_by=PROGRAM_ID)
    if programs.get('Q042-STOCKDIAG-V21') not in (PREVIOUS_ENTRY,historical):raise ValueError('V21_REGISTRY_PROVENANCE_GATE=FAIL')
    if PROGRAM_ID in programs and programs[PROGRAM_ID]!=ENTRY:raise ValueError('V22_REGISTRY_CONFLICT_GATE=FAIL')
    programs['Q042-STOCKDIAG-V21']=historical;programs[PROGRAM_ID]=ENTRY
    return data

def check_package(root):
    manifest=json.loads((root/'q042_durable_manifest_v22.json').read_text())
    if (manifest['q'],manifest['program_id'])!=('Q-042',PROGRAM_ID):raise ValueError('MANIFEST_IDENTITY_GATE=FAIL')
    for name,digest in manifest['files'].items():
        path=root/name
        if name==TARGET and not path.exists():path=root/'.github/workflows'/TARGET
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('PACKAGE_HASH_GATE=FAIL '+name)
    contract=json.loads((root/'q042_durable_contract_v22.json').read_text())
    if (contract['q'],contract['program_id'],contract['probe_seconds'],contract['new_bobyqa_starts'],contract['maximum_probe_count'],contract['maximum_class_point_count'],contract['production_restart_authorized'])!=('Q-042',PROGRAM_ID,14400,0,1,0,False):raise ValueError('FROZEN_BUDGET_GATE=FAIL')
    dependency=root/'q042_stock_diagnostic_v21.py'
    if not dependency.is_file() or hashlib.sha256(dependency.read_bytes()).hexdigest()!='c7a253a8a8d9965e7f9857b9124674d5dfb23b56ea604916e2943f4d5d88dd10':raise ValueError('REUSED_V21_HELPER_GATE=FAIL')
    return manifest

def install(root,check=False):
    root=Path(root);check_package(root)
    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    expected=json.loads((root/'q042_durable_manifest_v22.json').read_text())['permanent_launcher_sha256']
    if not launcher.is_file() or hashlib.sha256(launcher.read_bytes()).hexdigest()!=expected:raise ValueError('PERMANENT_LAUNCHER_HASH_GATE=FAIL')
    registry=root/'bubbleverse_program_registry.json';readme=root/'README.md'
    old_r=registry.read_bytes();old_m=readme.read_bytes()
    data=registry_update(json.loads(old_r));text=readme_update(old_m.decode())
    target=root/'.github/workflows'/TARGET;flat=root/TARGET
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=hashlib.sha256((flat if flat.exists() else target).read_bytes()).hexdigest():raise ValueError('TARGET_CONFLICT_GATE=FAIL')
    if check:
        if not target.is_file() or json.loads(old_r)!=data or text.encode()!=old_m:raise ValueError('LIVE_INSTALL_GATE=FAIL apply helper first')
    else:
        target.parent.mkdir(parents=True,exist_ok=True)
        old_target=target.read_bytes() if target.exists() else None
        try:
            if flat.exists():target.write_bytes(flat.read_bytes())
            registry.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');readme.write_text(text)
        except BaseException:
            registry.write_bytes(old_r);readme.write_bytes(old_m)
            if old_target is None:target.unlink(missing_ok=True)
            else:target.write_bytes(old_target)
            raise
    # Mirror the observed launcher's exact syntax gates; never evaluate user input.
    entry=json.loads(registry.read_text())['programs'][PROGRAM_ID]
    if entry['status']!='ACTIVE' or not re.fullmatch(r'Q-[0-9]{3,}',entry['q']) or not re.fullmatch(r'[A-Za-z0-9._-]+\.ya?ml',entry['workflow_id']) or entry['target_ref']!='main' or not target.is_file():raise ValueError('LAUNCHER_GATE=FAIL')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')
    print('NO_COMMIT_NO_DISPATCH')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--root',default='.');a=p.parse_args();install(a.root,a.check)
if __name__=='__main__':main()
