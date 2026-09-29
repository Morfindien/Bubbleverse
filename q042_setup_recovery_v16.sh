#!/usr/bin/env bash
set -euo pipefail

# Q042-PROD-V16 changes no science, sampler setting, seed, or checkpoint format.
# It replaces the disposable 10-minute canary resume probe with a real 240-minute
# relay segment that must persist semantic checkpoint progress before fan-out.
bash q042_setup_recovery_v15.sh

python - <<'PYV16'
import hashlib,json,pathlib
p=pathlib.Path('q042_runtime/q042_polychord_partial_init_v15_adoption.json')
if not p.is_file(): raise SystemExit('Q042_V16_V15_RUNTIME_ADOPTION_GATE=FAIL missing')
d=json.loads(p.read_text())
assert d.get('status')=='PASS', 'Q042_V16_V15_RUNTIME_STATUS_GATE=FAIL'
assert d.get('scientific_contract_changed') is False, 'Q042_V16_SCIENCE_GATE=FAIL'
assert d.get('checkpoint_interval')==25 and d.get('serial_only') is True, 'Q042_V16_CHECKPOINT_CONTRACT_GATE=FAIL'
assert d.get('patcher_sha256')=='22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6', 'Q042_V16_PATCHER_HASH_GATE=FAIL'
assert d.get('selftest_sha256')=='7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462', 'Q042_V16_SELFTEST_HASH_GATE=FAIL'
out={
 'q':'Q-042','program_id':'Q042-PROD-V16','stage':'V15_PARTIAL_INIT_RUNTIME_ADOPTION',
 'status':'PASS','scientific_result':False,'scientific_contract_changed':False,
 'inherited_runtime_adoption':str(p),'inherited_runtime_adoption_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'patcher_sha256':d['patcher_sha256'],'selftest_sha256':d['selftest_sha256'],
 'checkpoint_interval':25,'serial_only':True,
 'canary_relay_policy':'REAL_240_MIN_SEGMENT1_MUST_PERSIST_SEMANTIC_PROGRESS_BEFORE_FANOUT'
}
pathlib.Path('q042_runtime/q042_polychord_partial_init_v16_adoption.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V16_PARTIAL_INIT_ADOPTION_GATE=PASS')
PYV16
