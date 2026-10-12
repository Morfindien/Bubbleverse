"""Q048 candidate package, frozen backend and differential memory gates."""
from pathlib import Path
import hashlib,json
import q048_resume_v2 as e

def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def check(root=None):
    root=Path(root or e.ROOT);lock=e.load(root/'q048_resume_package_v2.json')
    if lock.get('program_id')!=e.ID or lock.get('q')!=e.Q:raise ValueError('PACKAGE_IDENTITY')
    for name,want in lock['files'].items():
        path=root/name
        if not path.is_file() or sha(path.read_bytes())!=want:raise ValueError('PACKAGE_FILE '+name)
    for name,want in lock['reused_git_blobs'].items():
        b=(root/name).read_bytes()
        if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=want:raise ValueError('PINNED_BACKEND '+name)
    registry=e.load(root/'bubbleverse_program_registry.json')['programs'];entry=registry[e.ID]
    prior={k:v for k,v in registry.items() if k!=e.ID}
    if len(prior)!=57 or sha(canonical(prior))!=lock['protected_registry_entries_sha256']:raise ValueError('REGISTRY_HISTORY')
    target='.github/workflows/q048-resume-v2.yml'
    if (entry.get('q')!=e.Q or entry.get('status')!='ACTIVE' or entry.get('version')!='v2'
        or entry.get('workflow_path')!=target or entry.get('workflow_id')!=Path(target).name
        or entry.get('config')!='q048_resume_config_v2.json' or entry.get('scientific_acceptance') is not False):raise ValueError('REGISTRY_TARGET_SCOPE')
    settings=e.load(root/'q048_resume_config_v2.json')
    if settings['source_config_sha256']!=e.digest(root/settings['source_config_file']) or settings['seed_sha256']!=e.digest(root/settings['seed_file']):raise ValueError('CONTROL_PIN')
    source=e.p.validate_config(e.load(root/settings['source_config_file']))
    for case,row in source['cases'].items():
        objects={'effective_background_hex.json':row['background'],'effective_precision.json':row['precision'],'thermal_starts_hex.jsonl':row['thermal_starts']}
        for name,obj in objects.items():
            b=(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in obj) if name.endswith('jsonl') else json.dumps(obj,separators=(',',':'))+'\n').encode()
            if sha(b)!=row['source_input_hashes'][name]:raise ValueError('CAPTURE_BYTES '+case+'/'+name)
        x=e.load(root/(case+'_checkpoint_v2.json'));m=x['metadata'];r=x['record']
        if (m['config_hash']!=e.objhash(settings) or m['case']!=case or r['source_input_hashes']!=row['source_input_hashes']
            or r['final_result_gate']!='UNRESOLVED' or r['actual_source_admission']!='UNRESOLVED'
            or r['scientific_question']!=source['scientific_question']):raise ValueError('SHIPPED_CHECKPOINT_IDENTITY')
    readme=(root/'README.md').read_text()
    for token in (e.ID,target,'CONDITIONAL_SOURCE_REAL_PREFIX','UNRESOLVED','.github/workflows/00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if token not in readme:raise ValueError('README_PATH_OR_SCOPE '+token)
    tail=lock['historical_journal_tail'];journal=(root/'Q047_SAMLET_JOURNAL.md').read_bytes()
    if len(journal)<tail['bytes'] or sha(journal[-tail['bytes']:])!=tail['sha256']:raise ValueError('JOURNAL_HISTORY')
    if source['scientific_question'].encode() not in journal:raise ValueError('EXACT_QUESTION_LOST')
    return {'q':e.Q,'program_id':e.ID,'package_gate':'PASS','launcher_gate':'PASS_CANDIDATE_LOCAL','readme_gate':'PASS_CANDIDATE_LOCAL','repository_consistency_gate':'PASS_CANDIDATE_LOCAL','remote_installation':'NOT_PERFORMED','final_result_gate':'UNRESOLVED'}
if __name__=='__main__':print(json.dumps(check()))
