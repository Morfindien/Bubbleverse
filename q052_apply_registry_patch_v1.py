from pathlib import Path
import argparse,json
p=argparse.ArgumentParser()
p.add_argument("--registry",default="bubbleverse_program_registry.json")
p.add_argument("--patch",default="q052_program_registry_patch_v1.json")
p.add_argument("--output",default="bubbleverse_program_registry.q052-v1.json")
a=p.parse_args()
r=json.loads(Path(a.registry).read_text());p0=json.loads(Path(a.patch).read_text())
pid=p0["program_id"]
if pid in r["programs"]: raise SystemExit("PROGRAM_ID_ALREADY_EXISTS")
r["programs"][pid]=p0["entry"]
Path(a.output).write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n")
print(a.output)
