#!/usr/bin/env bash
set -euo pipefail

# Q042-PROD-V15 changes no science and no checkpoint format.
# Reuse the V13 patch/relink/self-test implementation byte-for-byte, then
# fail closed on the exact manifest hashes that V13 actually writes.
bash q042_setup_recovery_v13.sh

python - <<'PYV15'
import hashlib, json, pathlib
p=pathlib.Path('q042_runtime/q042_polychord_partial_init_v13.json')
if not p.is_file(): raise SystemExit('Q042_V15_V13_RUNTIME_MANIFEST_GATE=FAIL missing')
d=json.loads(p.read_text())
expected_patcher='22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6'
expected_selftest='7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462'
assert d.get('status')=='PASS', 'Q042_V15_V13_RUNTIME_STATUS_GATE=FAIL'
assert d.get('base_commit')=='3ade6445bb3719a6db6f6e81f178765545ffc833', 'Q042_V15_POLYCHORD_COMMIT_GATE=FAIL'
assert d.get('checkpoint_interval')==25 and d.get('serial_only') is True, 'Q042_V15_CHECKPOINT_CONTRACT_GATE=FAIL'
assert d.get('patcher_sha256')==expected_patcher, 'Q042_V15_PATCHER_HASH_GATE=FAIL'
assert d.get('selftest_sha256')==expected_selftest, 'Q042_V15_SELFTEST_HASH_GATE=FAIL'
assert d.get('selftest_status')=='PASS' and d.get('selftest_exact_resume_byte_identity') is True, 'Q042_V15_REPRO_GATE=FAIL'
out={
 'q':'Q-042','program_id':'Q042-PROD-V15','stage':'V13_PARTIAL_INIT_RUNTIME_ADOPTION',
 'status':'PASS','scientific_result':False,'scientific_contract_changed':False,
 'inherited_runtime_manifest':str(p),'inherited_runtime_manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'patcher_sha256':expected_patcher,'selftest_sha256':expected_selftest,
 'checkpoint_interval':25,'serial_only':True,
}
pathlib.Path('q042_runtime/q042_polychord_partial_init_v15_adoption.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V15_PARTIAL_INIT_ADOPTION_GATE=PASS')
PYV15
