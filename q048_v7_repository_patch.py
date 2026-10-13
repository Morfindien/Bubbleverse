"""Differential repository patch for Q048-GUARDCONT-V7.

This script changes ONLY the Q048 V6/V7 registry relationship and prepends the
V7 README section.  It refuses to run unless registry and README are byte-exact
to Bubbleverse commit 2bc190aeb1a2659fbc9bc0d402159c7768c6b15a.  It never touches the permanent launcher.
"""
from pathlib import Path
import copy,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE_REGISTRY_BLOB='506349e0d5a8aa198849d31a3e0ee3804bf2e589'
BASE_README_BLOB='32b90d4927037fc4fe129e3931332277a269ec34'
NEW_ID='Q048-GUARDCONT-V7';OLD_ID='Q048-STRUCTURAL-V6'

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def main():
 rp=ROOT/'bubbleverse_program_registry.json';mp=ROOT/'README.md';section=(ROOT/'README_Q048_V7_SECTION.md').read_text()
 rb=rp.read_bytes();mb=mp.read_bytes();need(blob(rb)==BASE_REGISTRY_BLOB,'REGISTRY_BASE_CHANGED_RECONCILE_FIRST');need(blob(mb)==BASE_README_BLOB,'README_BASE_CHANGED_RECONCILE_FIRST')
 reg=json.loads(rb);programs=reg['programs'];need(NEW_ID not in programs,'V7_ALREADY_PRESENT');need(programs[OLD_ID]['status']=='ACTIVE','V6_NOT_ACTIVE_BASE')
 entry=json.loads((ROOT/'q048_v7_registry_entry.json').read_text());need(entry['program_id']==NEW_ID and entry['q']=='Q-048','ENTRY_IDENTITY')
 old=copy.deepcopy(programs[OLD_ID]);old['status']='SUPERSEDED';old['superseded_by']=NEW_ID;programs[OLD_ID]=old;programs[NEW_ID]=entry
 rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 mp.write_text(section+'\n---\n\n## Preserved historical repository context\n\n'+mb.decode())
 print('REPOSITORY_PATCH_GATE=PASS')
if __name__=='__main__':main()
