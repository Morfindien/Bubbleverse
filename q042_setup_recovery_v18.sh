#!/usr/bin/env bash
set -euo pipefail

# V18 does not change the V17/V13 PolyChord checkpoint implementation.
# First reproduce the exact proven V17 runtime and robust checkpoint self-test.
bash q042_setup_recovery_v17.sh

# Then prove the exact Cobaya 3.5.6 failure mode and the V18 detection adapter:
# without the adapter, Cobaya deletes a partial-only raw PolyChord directory;
# with the adapter, resume remains enabled and the partial checkpoint survives.
python q042_cobaya_partial_resume_adapter_v18.py \
  --selftest \
  --output q042_runtime/q042_cobaya_partial_resume_adapter_selftest_v18.json

python - <<'PYV18'
import hashlib,json,pathlib

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

parent=pathlib.Path('q042_runtime/q042_polychord_partial_init_v17.json')
ptest=json.loads(pathlib.Path('q042_runtime/q042_cobaya_partial_resume_adapter_selftest_v18.json').read_text())
assert parent.is_file(), 'Q042_V18_PARENT_RUNTIME_MANIFEST_GATE=FAIL'
p=json.loads(parent.read_text())
assert p.get('status')=='PASS'
assert p.get('checkpoint_interval')==25 and p.get('serial_only') is True
assert p.get('patcher_sha256')=='22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6'
assert p.get('selftest_sha256')=='1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9'
assert p.get('selftest_exact_resume_byte_identity') is True
assert ptest.get('status')=='PASS'
assert ptest.get('program_id')=='Q042-PROD-V18'
assert ptest.get('cobaya_version')=='3.5.6'
assert ptest.get('baseline_cleanup_observed') is True
assert ptest.get('adapted_resuming') is True
assert ptest.get('adapted_partial_checkpoint_preserved') is True

out={
 'q':'Q-042','program_id':'Q042-PROD-V18',
 'stage':'COBAYA_PARTIAL_INIT_RESUME_ADAPTER_RUNTIME_V18','status':'PASS',
 'scientific_result':False,'scientific_contract_changed':False,
 'cobaya_version':'3.5.6',
 'adapter_file':'q042_cobaya_partial_resume_adapter_v18.py',
 'adapter_sha256':'b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567',
 'baseline_cleanup_observed':True,
 'adapted_resuming':True,
 'adapted_partial_checkpoint_preserved':True,
 'inherited_partial_runtime_manifest':str(parent),
 'inherited_partial_runtime_manifest_sha256':sha(parent),
 'checkpoint_interval':25,
 'checkpoint_format_changed':False,
}
pathlib.Path('q042_runtime/q042_cobaya_partial_resume_adapter_v18.json').write_text(
 json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V18_COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_GATE=PASS')
PYV18
