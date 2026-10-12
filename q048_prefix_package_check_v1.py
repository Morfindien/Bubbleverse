"""Local installed-package/source/input/launcher/README consistency gates."""
from pathlib import Path
import hashlib, json
import q048_prefix_v1 as p
import q047_certificate_v1 as old

def check(root=None):
    root=Path(root or p.ROOT);lock=old.load(root/'q048_prefix_package_v1.json')
    if lock.get('program_id')!=p.ID or lock.get('q')!=p.Q:raise ValueError('PACKAGE_IDENTITY')
    for name,want in lock['files'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=want:raise ValueError('PACKAGE_HASH '+name)
    for name,sha in lock['reused_git_blobs'].items():
        data=(root/name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=sha:raise ValueError('PINNED_BACKEND_CHANGED '+name)
    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    if hashlib.sha256(launcher.read_bytes()).hexdigest()!=lock['launcher_sha256']:raise ValueError('UNCHANGED_LAUNCHER_HASH')
    registry=old.load(root/'bubbleverse_program_registry.json')['programs']
    entry=registry[p.ID];prior={k:v for k,v in registry.items() if k!=p.ID}
    protected=hashlib.sha256(json.dumps(prior,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    if protected!=lock['protected_registry_entries_sha256']:raise ValueError('EXISTING_REGISTRY_CHANGED')
    target='.github/workflows/q048-prefix-v1.yml'
    if entry.get('q')!=p.Q or entry.get('status')!='ACTIVE' or entry.get('version')!='v1' or entry.get('workflow_path')!=target or entry.get('workflow_id')!=Path(target).name:raise ValueError('REGISTRY_Q_VERSION_TARGET')
    c=p.validate_config(old.load(root/'q048_prefix_config_v1.json'))
    for case,row in c['cases'].items():
        objects={'effective_background_hex.json':row['background'],'effective_precision.json':row['precision'],'thermal_starts_hex.jsonl':row['thermal_starts']}
        for name,obj in objects.items():
            text=''.join(json.dumps(x,separators=(',',':'))+'\n' for x in obj) if name.endswith('jsonl') else json.dumps(obj,separators=(',',':'))+'\n'
            if hashlib.sha256(text.encode()).hexdigest()!=row['source_input_hashes'][name]:raise ValueError('CAPTURE_BYTES_CHANGED '+case+'/'+name)
    readme=(root/'README.md').read_text()
    for token in (p.ID,target,'CONDITIONAL_SOURCE_REAL_PREFIX','UNRESOLVED'):
        if token not in readme:raise ValueError('README_SCOPE_OR_PATH '+token)
    incoming=lock['historical_journal_tail'];journal=(root/'Q047_SAMLET_JOURNAL.md').read_bytes()
    if hashlib.sha256(journal[-incoming['bytes']:]).hexdigest()!=incoming['sha256']:raise ValueError('JOURNAL_HISTORY_CHANGED')
    if c['scientific_question'].encode() not in journal:raise ValueError('EXACT_QUESTION_LOST')
    return {'q':p.Q,'program_id':p.ID,'package_gate':'PASS','launcher_gate':'PASS_CANDIDATE_LOCAL',
            'readme_gate':'PASS_CANDIDATE_LOCAL','registry_gate':'PASS_CANDIDATE_LOCAL',
            'repository_consistency_gate':'PASS_CANDIDATE_LOCAL','remote_installation':'NOT_PERFORMED'}
if __name__=='__main__':print(json.dumps(check()))
