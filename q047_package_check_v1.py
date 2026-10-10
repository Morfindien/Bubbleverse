"""Q047 package/launcher/source/result gates; no campaign or native dispatch."""
from pathlib import Path
import argparse,hashlib,json,re,urllib.request
from fractions import Fraction as F
import q047_certificate_v1 as c

WORKFLOW='q047-certificate-check-v1.yml'
LAUNCHER='.github/workflows/00-bubbleverse-start.yml'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def resolve(registry,program_id):
    if not re.fullmatch(r'[A-Z0-9][A-Z0-9-]{2,63}',program_id):raise ValueError('PROGRAM_ID_SYNTAX')
    if program_id not in registry['programs']:raise ValueError('UNKNOWN_PROGRAM_ID')
    entry=registry['programs'][program_id]
    if entry.get('status')!='ACTIVE' or entry.get('q')!=c.Q:raise ValueError('REGISTRY_STATUS_OR_Q')
    if entry.get('workflow_id')!=WORKFLOW or entry.get('target_ref')!='main':raise ValueError('REGISTRY_TARGET')
    if entry.get('version')!='v1':raise ValueError('REGISTRY_VERSION')
    return entry

def verify_hashes(root):
    root=Path(root);manifest=c.load(root/'q047_package_v1.json')
    if manifest.get('q')!=c.Q or manifest.get('program_id')!=c.ID:raise ValueError('PACKAGE_IDENTITY')
    for name,digest in manifest['file_sha256'].items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts:raise ValueError('PACKAGE_PATH')
        if not (root/path).is_file() or sha(root/path)!=digest:raise ValueError('PACKAGE_HASH '+name)
    return manifest

def verify_inherited_registry(registry,manifest):
    keys=manifest['inherited_registry_keys']
    if len(set(keys))!=manifest['inherited_registry_entries'] or any(k not in registry['programs'] for k in keys):
        raise ValueError('INHERITED_REGISTRY_CHANGED')
    subset={k:registry['programs'][k] for k in keys}
    digest=hashlib.sha256(json.dumps(subset,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if digest!=manifest['inherited_registry_subset_sha256']:raise ValueError('INHERITED_REGISTRY_CHANGED')

def static(root):
    root=Path(root);manifest=verify_hashes(root)
    if sha(root/LAUNCHER)!=manifest['launcher_sha256']:raise ValueError('UNCHANGED_LAUNCHER_HASH')
    registry=c.load(root/'bubbleverse_program_registry.json');entry=resolve(registry,c.ID)
    verify_inherited_registry(registry,manifest)
    if entry!=manifest['registry_entry']:raise ValueError('REGISTRY_ENTRY_CHANGED')
    if not (root/entry['workflow_path']).is_file():raise ValueError('WORKFLOW_MISSING')
    readme=(root/'README.md').read_text()
    for text in [c.ID,LAUNCHER,'bubbleverse_program_registry.json','FINAL_RESULT_GATE=UNRESOLVED']:
        if text not in readme:raise ValueError('README_CONTEXT '+text)
    targets=c.load(root/'q047_targets_v1.json')
    if set(targets['cases'])!=set(c.CASES):raise ValueError('TARGET_COMPLETENESS')
    for case,v in targets['cases'].items():
        accepted=7.4735260009765625 if case.startswith('camspec') else 7.4987945556640625
        if v['accepted_z_reio']!=accepted or v['requested_input_identity']['original_sampled_vector']['parent_metadata']['combination']!='FULL':
            raise ValueError('TARGET_FIXED_INPUT '+case)
    return dict(q=c.Q,program_id=c.ID,package_gate='PASS',launcher_gate='PASS',readme_gate='PASS',
      repository_consistency_gate='PASS',source_equivalence_gate='UNQUALIFIED',new_native_evaluations=0)

def sources(root,source_dir=None):
    root=Path(root);manifest=verify_hashes(root);checked={}
    for name,digest in manifest['native_source_sha256'].items():
        if source_dir:
            data=(Path(source_dir)/name).read_bytes()
        else:
            url='https://raw.githubusercontent.com/mwt5345/class_ede/'+c.SOURCE+'/'+name
            with urllib.request.urlopen(url,timeout=20) as r:data=r.read(2_000_001)
            if len(data)>2_000_000:raise ValueError('SOURCE_SIZE_CAP')
        if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('NATIVE_SOURCE_HASH '+name)
        checked[name]=digest
    return {'q':c.Q,'program_id':c.ID,'source_commit':c.SOURCE,'source_hash_gate':'PASS',
            'checked':checked,'source_to_binary_equivalence':'NOT_ESTABLISHED'}

def results(directory):
    directory=Path(directory)
    required=['q047_certificate_final_v1.json','q047_required_inputs_v1.json','q047_conditional_control_v1.json','q047_regional_controls_v1.json']
    if any(not (directory/n).is_file() for n in required):raise ValueError('OUTPUT_COMPLETENESS')
    final,needed,conditional,regional=[c.load(directory/n) for n in required]
    if any(v.get('q')!=c.Q or v.get('program_id')!=c.ID for v in [final,needed,conditional]):raise ValueError('OUTPUT_IDENTITY')
    if final.get('final_result_gate')!='UNRESOLVED' or final.get('new_native_evaluations')!=0:raise ValueError('FALSE_SCIENTIFIC_CLOSURE')
    if final.get('execution_status')!='COMPLETE':raise ValueError('JOB_COMPLETENESS')
    if conditional!=final['manufactured_conditional_control'] or needed['cases']!=final['input_admission']:
        raise ValueError('RESULT_COMPATIBILITY')
    if set(final['actual_applicability'])!=set(c.CASES) or any(v!='INSUFFICIENT_EVIDENCE' for v in final['actual_applicability'].values()):
        raise ValueError('FALSE_ACTUAL_APPLICABILITY')
    if conditional['conditional_event_gate']!='PASS' or conditional['scope']!='CONDITIONAL_LOCAL_UPPER_IVP':
        raise ValueError('CONDITIONAL_CONTROL_FAILURE')
    if regional.get('new_cosmology_evaluations')!=0 or set(regional['local_certificates'])!=set(c.CASES):raise ValueError('REGIONAL_COMPLETENESS')
    for case,v in regional['local_certificates'].items():
        if not v['contraction_verified_on_box'] or F(v['weighted_log_norm_upper'])>=-230 or not v['fd_inside_interval_derivatives']:
            raise ValueError('REGIONAL_STABILITY '+case)
    if F(regional['D_epsilon_upper_bound']['hi_exact'])>=F('-9.91e-7'):raise ValueError('REGIONAL_BOUNDARY')
    if F(regional['temperature_damping_fraction_loss_upper']['hi_exact'])>=F('.193'):raise ValueError('REGIONAL_DAMPING')
    return {'q':c.Q,'program_id':c.ID,'execution_status':'COMPLETE','tests_status':'COMPLETE',
      'technical_result_gate':'PASS','final_result_gate':'UNRESOLVED','result_status':'TECHNICAL_QUALIFICATION_ONLY',
      'output_sha256':{n:sha(directory/n) for n in required},'conditional_scope':'Local assumed IVP only; no actual first-hit certificate'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['static','sources','results'])
    parser.add_argument('--root',default=str(c.ROOT));parser.add_argument('--source-dir');parser.add_argument('--directory',default='q047_results')
    args=parser.parse_args()
    if args.mode=='static':result=static(args.root)
    elif args.mode=='sources':result=sources(args.root,args.source_dir)
    else:result=results(args.directory)
    out=Path(args.directory)/('q047_'+args.mode+'_gate_v1.json');c.write(out,result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
