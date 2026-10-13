"""Q048 V7 exact executable pins plus differential mutable-repository validation."""
from pathlib import Path
import copy,hashlib,json,os,re,subprocess,tempfile,textwrap
import q048_guard_continuation_v7 as e

def sha256(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def check(root=None):
 root=Path(root or e.ROOT);lock=e.old.load(root/'q048_guard_package_v7.json');s=e.validate_sources();e.fail(lock['program_id']==e.ID and lock['q']==e.Q,'PACKAGE_IDENTITY')
 for n,want in lock['files'].items():e.fail((root/n).is_file() and sha256(root/n)==want,'PACKAGE_FILE '+n)
 reg=e.old.load(root/'bubbleverse_program_registry.json');programs=reg['programs'];entry=programs[e.ID]
 for k,v in lock['registry_entry'].items():e.fail(entry.get(k)==v,'REGISTRY_ENTRY '+k)
 e.fail(programs['Q048-STRUCTURAL-V6'].get('status')=='SUPERSEDED' and programs['Q048-STRUCTURAL-V6'].get('superseded_by')==e.ID,'REGISTRY_V6_SUPERSESSION')
 # Reconstruct the exact pre-V7 registry and verify its Git blob: no unrelated entry may have changed.
 base=copy.deepcopy(reg);base['programs'].pop(e.ID);oldv6=base['programs']['Q048-STRUCTURAL-V6'];oldv6['status']='ACTIVE';oldv6.pop('superseded_by',None)
 raw=(json.dumps(base,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();e.fail(blob(raw)==s['repository_mutable_base']['bubbleverse_program_registry.json_git_blob_sha1'],'REGISTRY_UNRELATED_CHANGE')
 section=(root/'README_Q048_V7_SECTION.md').read_text();readme=(root/'README.md').read_text();prefix=section+'\n---\n\n## Preserved historical repository context\n\n'
 e.fail(readme.startswith(prefix),'README_PREFIX');historical=readme[len(prefix):].encode();e.fail(blob(historical)==s['repository_mutable_base']['README.md_git_blob_sha1'],'README_HISTORY_CHANGED')
 for token in [e.ID,'.github/workflows/q048-guard-continuation-v7.yml',e.SCOPE,'UNRESOLVED','.github/workflows/00-bubbleverse-start.yml','bubbleverse_program_registry.json']:e.fail(token in readme,'README_REFERENCE '+token)
 launcher=root/'.github/workflows/00-bubbleverse-start.yml';e.fail(e.git_blob_sha1(launcher)==s['reused_git_blob_sha1']['.github/workflows/00-bubbleverse-start.yml'],'LAUNCHER_CHANGED')
 script=textwrap.dedent(re.search(r"python - <<'PY'\n(.*?)\n\s*PY",launcher.read_text(),re.S).group(1))
 for value,success in [(e.ID,True),('Q048-STRUCTURAL-V6',False),('Q999-UNKNOWN',False),(e.ID+';echo bad',False),('$(touch bad)',False)]:
  with tempfile.NamedTemporaryFile() as output:
   env=dict(os.environ,RAW_PROGRAM_ID=value,GITHUB_OUTPUT=output.name);r=subprocess.run(['python3','-c',script],cwd=root,env=env,capture_output=True,text=True,timeout=10)
   e.fail((r.returncode==0)==success,'LAUNCHER_INPUT_GATE')
   if success:
    fields=dict(x.split('=',1) for x in Path(output.name).read_text().splitlines());e.fail(fields['workflow_id']=='q048-guard-continuation-v7.yml' and fields['q']==e.Q,'LAUNCHER_RESOLUTION')
 return {'q':e.Q,'program_id':e.ID,'package_gate':'PASS','launcher_gate':'PASS_LOCAL_INSTALLATION','readme_gate':'PASS_LOCAL_INSTALLATION','journal_continuity_gate':'PASS','repository_consistency_gate':'PASS_LOCAL_INSTALLATION','remote_installation':'NOT_PERFORMED','final_result_gate':'UNRESOLVED'}
if __name__=='__main__':print(json.dumps(check()))
