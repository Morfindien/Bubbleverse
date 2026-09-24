#!/usr/bin/env python3
"""Local helper: add Q042 registry entry without modifying any existing registry entry."""
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--registry',default='bubbleverse_program_registry.json'); ap.add_argument('--patch',default='q042_program_registry_patch_v1.json'); ap.add_argument('--output',default='bubbleverse_program_registry.q042-v1.json'); a=ap.parse_args()
reg=json.loads(Path(a.registry).read_text(encoding='utf-8')); patch=json.loads(Path(a.patch).read_text(encoding='utf-8'))
programs=reg.setdefault('programs',{}); entry=patch['entry']
for k,v in entry.items():
    if k in programs: raise SystemExit(f'PROGRAM_ID_GATE=FAIL already exists: {k}')
    programs[k]=v
Path(a.output).write_text(json.dumps(reg,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'REGISTRY_PATCH_GATE=PASS output={a.output}')
