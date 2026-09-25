#!/usr/bin/env bash
set -euo pipefail
bash q042_setup_v11.sh
python - <<'PYSETUP'
import json,pathlib
src=pathlib.Path('q042_runtime/q042_external_runtime_provenance_v11.json')
d=json.loads(src.read_text())
assert d.get('polychord_commit')=='3ade6445bb3719a6db6f6e81f178765545ffc833', 'POLYCHORD_EXACT_COMMIT_GATE=FAIL'
assert d.get('pantheonplus_manifest_sha256') and d.get('pantheonplus_runtime_files'), 'PANTHEONPLUS_MANIFEST_GATE=FAIL'
d.update({'q':'Q-042','case_id':'NOT DOCUMENTED','program_id':'Q042-PROD-V1','run_id':'Q042-PRODUCTION-PORTABILITY-V1','result_id':'R-Q042-PRODUCTION-PORTABILITY-001','technical_parent_program_id':'Q042-PREFLIGHT-V11','technical_repair':'NONE_PRODUCTION_REUSES_V11_VALIDATED_RUNTIME','scientific_result':False})
out=pathlib.Path('q042_runtime/q042_external_runtime_provenance_prod_v1.json');out.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V1_RUNTIME_SOURCE_GATE=PASS')
PYSETUP
