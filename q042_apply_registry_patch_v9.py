#!/usr/bin/env python3
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--registry',default='bubbleverse_program_registry.json');p.add_argument('--patch',default='q042_program_registry_patch_v9.json');p.add_argument('--output',default='bubbleverse_program_registry.q042-v5.json');a=p.parse_args()
r=json.loads(pathlib.Path(a.registry).read_text());q=json.loads(pathlib.Path(a.patch).read_text());progs=r.setdefault('programs',{})
for k,v in q['entry'].items():
    if k in progs: raise SystemExit(f'REGISTRY_ADD_GATE=FAIL already_exists={k}')
    progs[k]=v
pathlib.Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print('REGISTRY_ADD_GATE=PASS '+','.join(q['entry']))
