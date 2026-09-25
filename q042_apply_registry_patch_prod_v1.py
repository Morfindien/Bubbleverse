#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--registry',default='bubbleverse_program_registry.json');p.add_argument('--patch',default='q042_program_registry_patch_prod_v1.json');a=p.parse_args()
    rp=Path(a.registry);pp=Path(a.patch)
    reg=json.loads(rp.read_text(encoding='utf-8'));patch=json.loads(pp.read_text(encoding='utf-8'))
    programs=reg.setdefault('programs',{})
    for pid,entry in patch.get('patch',{}).items():
        if pid in programs and programs[pid]!=entry:
            raise SystemExit(f'REGISTRY_COLLISION_GATE=FAIL program_id={pid}')
        programs[pid]=entry
    rp.write_text(json.dumps(reg,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Q042_PROD_V1_REGISTRY_PATCH_GATE=PASS program_id=Q042-PROD-V1')
if __name__=='__main__':main()
