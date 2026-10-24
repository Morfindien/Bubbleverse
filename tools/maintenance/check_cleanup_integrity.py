"""Read-only cleanup verification. Never import or execute scientific programs."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import unicodedata

DEFAULT_RUN = 'docs/maintenance/cleanup/20261024-b99a5c7-v330'

def safe_path(root, relative):
    path=PurePosixPath(relative)
    if not relative or path.is_absolute() or '..' in path.parts or '\\' in relative:
        raise ValueError('unsafe relative path: '+relative)
    root=Path(root).resolve(); candidate=root.joinpath(*path.parts)
    if not candidate.resolve().is_relative_to(root):
        raise ValueError('symlink escape: '+relative)
    return candidate

def metadata(path):
    path=Path(path)
    if not path.exists() and not path.is_symlink():raise ValueError('missing file: '+str(path))
    s=path.lstat(); link=path.is_symlink()
    if not (stat.S_ISREG(s.st_mode) or stat.S_ISLNK(s.st_mode)):
        raise ValueError('unsupported file type: '+str(path))
    h=hashlib.sha256()
    if link:h.update(os.readlink(path).encode())
    else:
        with path.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return {'sha256':h.hexdigest(),'size':s.st_size,'permissions':stat.S_IMODE(s.st_mode),
            'file_type':'symlink' if link else 'regular','symlink_target':os.readlink(path) if link else None}

def verify_record(root, record):
    path=safe_path(root,record['path']);actual=metadata(path)
    for key,value in actual.items():
        if record[key]!=value:raise ValueError('integrity mismatch '+record['path']+' '+key)

def validate_schema_definition(schema):
    known={'$schema','$id','title','description','type','required','properties','items','enum','pattern','minimum','minItems','additionalProperties'}
    if set(schema)-known:raise ValueError('unsupported schema keywords '+str(set(schema)-known))
    for sub in schema.get('properties',{}).values():validate_schema_definition(sub)
    if 'items' in schema:validate_schema_definition(schema['items'])

def schema_check(obj, schema, location='$'):
    # Deliberately limited, fail-closed JSON Schema subset; no dependency install.
    validate_schema_definition(schema)
    kind=schema.get('type')
    types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'boolean':bool,'null':type(None)}
    if kind:
        options=kind if isinstance(kind,list) else [kind]
        good=any(isinstance(obj,types[k]) and not (isinstance(obj,bool) and k in ('integer','number')) for k in options)
        if not good:raise ValueError(location+' type')
    if 'enum' in schema and obj not in schema['enum']:raise ValueError(location+' enum')
    if 'pattern' in schema and (not isinstance(obj,str) or re.search(schema['pattern'],obj) is None):raise ValueError(location+' pattern')
    if 'minimum' in schema and obj<schema['minimum']:raise ValueError(location+' minimum')
    if isinstance(obj,dict):
        for key in schema.get('required',[]):
            if key not in obj:raise ValueError(location+' missing '+key)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False and set(obj)-set(props):raise ValueError(location+' additional properties')
        for key,sub in props.items():
            if key in obj:schema_check(obj[key],sub,location+'.'+key)
    if isinstance(obj,list):
        if len(obj)<schema.get('minItems',0):raise ValueError(location+' minItems')
        for i,value in enumerate(obj):
            if 'items' in schema:schema_check(value,schema['items'],location+'['+str(i)+']')

def coverage(expected, rows):
    paths=[row['path'] for row in rows]
    if len(set(paths))!=len(paths) or set(paths)!=set(expected):raise ValueError('placement coverage mismatch')

def contract_coverage(baseline, placements, protected, entries, source_pairs, program_pairs):
    coverage(baseline,placements)
    expected={r['path'] for r in placements if r['protection_classification']=='PROTECTED'}
    actual=[r['path'] for r in protected]
    if len(actual)!=len(set(actual)) or set(actual)!=expected:raise ValueError('protected inventory coverage mismatch')
    if not source_pairs <= {(r['source'],r['kind']) for r in entries}:raise ValueError('entry source coverage mismatch')
    actual_programs={(r.get('registry_source'),r.get('program_id')) for r in entries if r.get('program_id')}
    if not program_pairs <= actual_programs:raise ValueError('registry program coverage mismatch')

def validate(root, run=DEFAULT_RUN):
    root=Path(root).resolve();folder=safe_path(root,run)
    load=lambda name:json.loads((folder/name).read_text())
    contracts=load('CONTRACTS.json')
    for name,schema in contracts['contracts'].items():schema_check(load(name),schema)
    inv=load('PROTECTED_INVENTORY.json');rel=load('RELOCATION_MANIFEST.json')
    coverage(rel['baseline_paths'],rel['files'])
    for name,rows,key in [('protected',inv['records'],'record_id'),('placement',rel['files'],'operation_id')]:
        ids=[row[key] for row in rows]
        if len(ids)!=len(set(ids)):raise ValueError('duplicate '+name+' IDs')
    for row in inv['records']:verify_record(root,row)
    for row in rel['files']:
        p=safe_path(root,row['new_path'])
        if metadata(p)['sha256']!=row['expected_destination_hash']:raise ValueError('placement hash '+row['new_path'])
        if row['operation']=='MOVE' and safe_path(root,row['path']).exists():raise ValueError('unexplained old path duplicate')
    entries=load('ENTRYPOINT_REGISTRY.json')['entries']
    base=rel['base_sha']
    git_paths=subprocess.check_output(['git','ls-tree','-rz','--name-only',base],cwd=root).decode().split('\0')[:-1]
    source_pairs=set();program_pairs=set()
    for p in git_paths+['tools/maintenance/check_cleanup_integrity.py','tests/maintenance/test_cleanup_integrity.py']:
        if p.endswith('.py'):source_pairs.add((p,'python'))
        elif p.endswith('.sh'):source_pairs.add((p,'shell'))
        elif p.endswith(('.yml','.yaml')) and re.search(r'^jobs:',safe_path(root,p).read_text(),re.M):source_pairs.add((p,'workflow'))
        if Path(p).name.startswith('bubbleverse_program_registry') and p.endswith('.json'):
            obj=json.loads(safe_path(root,p).read_text())
            for pid in obj.get('programs',{}):program_pairs.add((p,pid))
    contract_coverage(git_paths,rel['files'],inv['records'],entries,source_pairs,program_pairs)
    ids=[row['entry_id'] for row in entries]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate entry IDs')
    for row in entries:
        if not safe_path(root,row['source']).is_file():raise ValueError('missing entry source '+row['source'])
    paths=[p.relative_to(root).as_posix() for p in root.rglob('*') if '.git' not in p.relative_to(root).parts and p.is_file()]
    folded={}
    for p in paths:
        key=unicodedata.normalize('NFC',p).casefold()
        if key in folded and folded[key]!=p:raise ValueError('case/Unicode collision '+p)
        folded[key]=p
    return {'status':'PASS','protected_files':len(inv['records']),'placement_files':len(rel['files']),
            'entrypoints':len(entries),'schemas':len(contracts['contracts']),
            'scope':'Hashes, paths, metadata, placement, entry sources, supported schema subset and collisions; no scientific execution.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument('--run',default=DEFAULT_RUN)
    args=parser.parse_args()
    try:print(json.dumps(validate(args.root,args.run),indent=2))
    except (ValueError,KeyError,OSError,TypeError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}));return 1
    return 0

if __name__=='__main__':sys.exit(main())
