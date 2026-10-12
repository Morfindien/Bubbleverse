"""Exact installed executable pins and semantic mutable-repository validation."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile,textwrap
import q048_structural_v6 as e

def sha(b):return hashlib.sha256(b).hexdigest()
def check(root=None):
 root=Path(root or e.ROOT);lock=e.old.load(root/'q048_structural_package_v6.json');e.validate_sources()
 e.fail(lock['program_id']==e.ID and lock['q']==e.Q,'PACKAGE_IDENTITY')
 for n,want in lock['files'].items():e.fail((root/n).is_file()and sha((root/n).read_bytes())==want,'PACKAGE_FILE '+n)
 for case in e.p.CASES:e.parent_checkpoint(case)
 registry=e.old.load(root/'bubbleverse_program_registry.json')['programs'];entry=registry[e.ID]
 target='.github/workflows/q048-structural-v6.yml'
 for k,v in {'q':e.Q,'status':'ACTIVE','version':'v6','program_version':'v6','workflow_version':'v6','workflow_path':target,'workflow_id':'q048-structural-v6.yml','scientific_program':'q048_structural_runner_v6.py','config':'q048_structural_config_v6.json','scientific_acceptance':False}.items():e.fail(entry.get(k)==v,'REGISTRY_TARGET '+k)
 previous=e.old.load(root/'registry_original_v6.json')['programs']if(root/'registry_original_v6.json').exists()else lock['original_registry']
 expected=dict(previous);v5=dict(expected['Q048-RESUME-V5']);v5.update(status='SUPERSEDED',superseded_by=e.ID);expected['Q048-RESUME-V5']=v5
 protected={k:v for k,v in registry.items()if k!=e.ID};e.fail(protected==expected,'REGISTRY_HISTORY')
 readme=(root/'README.md').read_text()
 for token in [e.ID,target,e.SCOPE,'UNRESOLVED','.github/workflows/00-bubbleverse-start.yml','bubbleverse_program_registry.json']:e.fail(token in readme,'README_REFERENCE '+token)
 for n in lock['install_files']:e.fail((root/n).is_file(),'INSTALL_FILE '+n)
 journal=(root/'Q047_SAMLET_JOURNAL.md').read_bytes();tail=lock['journal_tail']
 e.fail(len(journal)>=tail['bytes']and sha(journal[-tail['bytes']:])==tail['sha256'],'JOURNAL_HISTORY')
 e.fail(e.config()['scientific_question'].encode()in journal,'JOURNAL_QUESTION')
 launcher_path=root/'.github/workflows/00-bubbleverse-start.yml'
 e.fail(sha(launcher_path.read_bytes())==lock['launcher_unchanged_sha256'],'LAUNCHER_SOURCE_CHANGED')
 launcher=launcher_path.read_text();script=textwrap.dedent(re.search(r"python - <<'PY'\n(.*?)\n\s*PY",launcher,re.S).group(1))
 for value,success in [(e.ID,True),('Q048-RESUME-V5',False),('Q999-UNKNOWN',False),(e.ID+';echo bad',False),('$(touch bad)',False),(e.ID+'\nfoo',False)]:
  with tempfile.NamedTemporaryFile()as output:
   env=dict(os.environ,RAW_PROGRAM_ID=value,GITHUB_OUTPUT=output.name)
   r=subprocess.run(['python3','-c',script],cwd=root,env=env,capture_output=True,text=True,timeout=10)
   e.fail((r.returncode==0)==success,'LAUNCHER_INPUT_GATE')
   if success:
    fields=dict(line.split('=',1)for line in Path(output.name).read_text().splitlines());e.fail(fields.get('workflow_id')=='q048-structural-v6.yml'and fields.get('q')==e.Q,'LAUNCHER_RESOLUTION')
 return {'q':e.Q,'program_id':e.ID,'package_gate':'PASS','launcher_gate':'PASS_LOCAL_INSTALLATION',
  'readme_gate':'PASS_LOCAL_INSTALLATION','journal_continuity_gate':'PASS','repository_consistency_gate':'PASS_LOCAL_INSTALLATION',
  'remote_installation':'NOT_PERFORMED','final_result_gate':'UNRESOLVED'}
if __name__=='__main__':print(json.dumps(check()))
