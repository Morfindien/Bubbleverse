"""Fail-closed differential repository installer/verifier for Q048-THRESHOLD-V9.

Canonical mutable base inspected at Bubbleverse HEAD
cf7b9fe835cd97cc01dbee99cd8f0ed69a399beb:

  Q048-PHASETURN-V8 = ACTIVE

This patch performs only:

  Q048-PHASETURN-V8 -> SUPERSEDED by Q048-THRESHOLD-V9
  Q048-THRESHOLD-V9 -> ACTIVE
  README.md -> prepend exact V9 current-architecture section

The permanent launcher is never modified.  --verify-only refuses to install and
is used by the scientific workflow after the one-time installer has completed.
"""
from pathlib import Path
import argparse, copy, hashlib, json

ROOT=Path(__file__).resolve().parent
BASE_REGISTRY_BLOB='3a9be5e054e837a736034df7dad4d636f1c50340'
BASE_README_BLOB='dcbeaba64b5e0d53d2ea64d895b51fb03862c9d6'
V8='Q048-PHASETURN-V8'
V9='Q048-THRESHOLD-V9'
SEP='\n---\n\n## Preserved historical repository context\n\n'


def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def need(x,msg):
    if not x:
        raise ValueError(msg)


def prefix():
    return (ROOT/'README_Q048_V9_SECTION.md').read_text()+SEP


def verify_installed(reg,readme):
    p=reg['programs']
    need(V8 in p and V9 in p,'V9_INSTALL_ENTRIES')
    need(p[V9]['status']=='ACTIVE' and p[V9].get('supersedes')==V8,'V9_ACTIVE_STATE')
    need(p[V8]['status']=='SUPERSEDED' and p[V8].get('superseded_by')==V9,'V8_SUPERSESSION_STATE')
    pre=prefix()
    need(readme.startswith(pre),'README_V9_PREFIX')
    historical=readme[len(pre):].encode()
    need(blob(historical)==BASE_README_BLOB,'README_HISTORICAL_BASE_CHANGED')
    base=copy.deepcopy(reg)
    base['programs'].pop(V9)
    v8=base['programs'][V8]
    v8['status']='ACTIVE'
    v8.pop('superseded_by',None)
    raw=(json.dumps(base,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    need(blob(raw)==BASE_REGISTRY_BLOB,'REGISTRY_HISTORICAL_BASE_CHANGED')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--verify-only',action='store_true')
    a=ap.parse_args()
    rp=ROOT/'bubbleverse_program_registry.json';mp=ROOT/'README.md'
    rb=rp.read_bytes();mb=mp.read_bytes()
    reg=json.loads(rb);readme=mb.decode()
    if V9 in reg.get('programs',{}):
        verify_installed(reg,readme)
        print('REPOSITORY_PATCH_GATE=PASS_ALREADY_INSTALLED')
        return
    if a.verify_only:
        raise ValueError('V9_NOT_INSTALLED_RUN_INSTALLER')
    need(blob(rb)==BASE_REGISTRY_BLOB,'REGISTRY_BASE_CHANGED_RECONCILE_FIRST')
    need(blob(mb)==BASE_README_BLOB,'README_BASE_CHANGED_RECONCILE_FIRST')
    p=reg['programs'];need(V8 in p,'V8_MISSING')
    need(p[V8]['status']=='ACTIVE','V8_NOT_ACTIVE_BASE')
    e9=json.loads((ROOT/'q048_v9_registry_entry.json').read_text())
    need(e9.get('program_id')==V9 and e9.get('q')=='Q-048' and e9.get('supersedes')==V8,'V9_ENTRY_IDENTITY')
    old=copy.deepcopy(p[V8]);old['status']='SUPERSEDED';old['superseded_by']=V9;p[V8]=old
    p[V9]=copy.deepcopy(e9)
    rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    mp.write_text(prefix()+readme)
    verify_installed(json.loads(rp.read_text()),mp.read_text())
    print('REPOSITORY_PATCH_GATE=PASS')


if __name__=='__main__':
    main()
