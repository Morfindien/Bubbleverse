"""Differential repository patch for Q048-PHASETURN-V8.

The inspected remote repository at c9ca98f... still has Q048-STRUCTURAL-V6 as
ACTIVE and contains the V7 registry-entry/README-section files without having
installed them into the canonical registry/README.  This patch reconciles that
history in one fail-closed operation:

  V6 -> SUPERSEDED by V7
  V7 -> installed as SUPERSEDED by V8
  V8 -> ACTIVE

The permanent launcher is never modified.  The patch is idempotent only for the
exact installed V8 state; unrelated registry/README changes require explicit
reconciliation rather than silent overwrite.
"""
from pathlib import Path
import copy,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE_REGISTRY_BLOB='506349e0d5a8aa198849d31a3e0ee3804bf2e589'
BASE_README_BLOB='32b90d4927037fc4fe129e3931332277a269ec34'
V6='Q048-STRUCTURAL-V6';V7='Q048-GUARDCONT-V7';V8='Q048-PHASETURN-V8'
SEP='\n---\n\n## Preserved historical repository context\n\n'

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)

def expected_prefix():
    s8=(ROOT/'README_Q048_V8_SECTION.md').read_text()
    s7=(ROOT/'README_Q048_V7_SECTION.md').read_text()
    return s8+SEP+s7+SEP

def verify_installed(reg,readme):
    p=reg['programs'];need(V8 in p and V7 in p and V6 in p,'V8_INSTALL_ENTRIES')
    need(p[V8]['status']=='ACTIVE' and p[V8].get('supersedes')==V7,'V8_ACTIVE_STATE')
    need(p[V7]['status']=='SUPERSEDED' and p[V7].get('superseded_by')==V8,'V7_SUPERSESSION_STATE')
    need(p[V6]['status']=='SUPERSEDED' and p[V6].get('superseded_by')==V7,'V6_SUPERSESSION_STATE')
    need(readme.startswith(expected_prefix()),'README_V8_V7_PREFIX')

def main():
    rp=ROOT/'bubbleverse_program_registry.json';mp=ROOT/'README.md'
    rb=rp.read_bytes();mb=mp.read_bytes();reg=json.loads(rb);readme=mb.decode()
    if V8 in reg.get('programs',{}):
        verify_installed(reg,readme);print('REPOSITORY_PATCH_GATE=PASS_ALREADY_INSTALLED');return
    need(blob(rb)==BASE_REGISTRY_BLOB,'REGISTRY_BASE_CHANGED_RECONCILE_FIRST')
    need(blob(mb)==BASE_README_BLOB,'README_BASE_CHANGED_RECONCILE_FIRST')
    p=reg['programs'];need(V7 not in p,'V7_UNEXPECTEDLY_INSTALLED');need(p[V6]['status']=='ACTIVE','V6_NOT_ACTIVE_BASE')
    e7=json.loads((ROOT/'q048_v7_registry_entry.json').read_text());e8=json.loads((ROOT/'q048_v8_registry_entry.json').read_text())
    need(e7.get('program_id')==V7 and e7.get('q')=='Q-048','V7_ENTRY_IDENTITY')
    need(e8.get('program_id')==V8 and e8.get('q')=='Q-048' and e8.get('supersedes')==V7,'V8_ENTRY_IDENTITY')
    old=copy.deepcopy(p[V6]);old['status']='SUPERSEDED';old['superseded_by']=V7;p[V6]=old
    e7=copy.deepcopy(e7);e7['status']='SUPERSEDED';e7['superseded_by']=V8;p[V7]=e7;p[V8]=e8
    rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    mp.write_text(expected_prefix()+readme)
    verify_installed(json.loads(rp.read_text()),mp.read_text())
    print('REPOSITORY_PATCH_GATE=PASS')
if __name__=='__main__':main()
