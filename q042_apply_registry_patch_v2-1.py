#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--registry',default='bubbleverse_program_registry.json');p.add_argument('--patch',default='q042_program_registry_patch_v2.json');p.add_argument('--output',default='bubbleverse_program_registry.q042-v2.json');a=p.parse_args()
r=json.loads(Path(a.registry).read_text(encoding='utf-8'));x=json.loads(Path(a.patch).read_text(encoding='utf-8'));programs=r.setdefault('programs',{})
for pid,entry in x['entry'].items():
 if pid in programs:raise SystemExit(f'ADD_ONLY_GATE=FAIL already_exists={pid}')
 programs[pid]=entry
Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(f'REGISTRY_PATCH_GATE=PASS output={a.output}')
