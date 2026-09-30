#!/usr/bin/env bash
set -euo pipefail

# Q042-PROD-V17 is a deployment/test-harness repair only.
# Recreate the frozen V1/V8 science runtime, apply the unchanged V13 partial-init
# patch, force relink, then run the robust V17 checkpoint-capture self-test.
bash q042_setup_recovery_v8.sh

python q042_patch_polychord_partial_init_v13.py   --root external/PolyChordLite   --manifest q042_runtime/q042_polychord_partial_init_source_v17.json

POLY="$PWD/external/PolyChordLite"
test "$(git -C "$POLY" rev-parse HEAD)" = "3ade6445bb3719a6db6f6e81f178765545ffc833"

rm -f "$POLY/lib/libchord.so" "$POLY/lib/libchord.a"
make -C "$POLY/src/polychord" clean
make -C "$POLY" -e libchord.so MPI=1
test -s "$POLY/lib/libchord.so"

NM_OUT="$(nm "$POLY/lib/libchord.so")"
grep -qi 'q042_write_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_WRITE_SYMBOL_GATE=FAIL'; exit 71; }
grep -qi 'q042_read_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_READ_SYMBOL_GATE=FAIL'; exit 72; }
grep -qi 'q042_delete_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_DELETE_SYMBOL_GATE=FAIL'; exit 73; }
echo 'Q042_POLYCHORD_PATCHED_BINARY_SYMBOL_GATE=PASS'

python -m pip install --disable-pip-version-check --force-reinstall --no-build-isolation --no-deps "$POLY"

python q042_polychord_partial_init_selftest_v17.py   --output q042_runtime/q042_polychord_partial_init_selftest_v17.json

python - <<'PYV17'
import hashlib,json,pathlib

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

src=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_source_v17.json').read_text())
st=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_selftest_v17.json').read_text())
assert src['status']=='PASS'
assert src['base_commit']=='3ade6445bb3719a6db6f6e81f178765545ffc833'
assert src['checkpoint_interval']==25 and src['serial_only'] is True
assert st['status']=='PASS' and st['exact_resume_byte_identity'] is True
assert st['program_id']=='Q042-PROD-V17'
assert st['capture_method']=='ATOMIC_META_AND_BINARY_DETECT_SIGSTOP_THEN_SIGKILL'
assert int(st['capture_attempt_used']) >= 1 and int(st['capture_attempt_used']) <= 3

gen=pathlib.Path(src['generate_file'])
nested=pathlib.Path(src['nested_sampling_file'])
lib=pathlib.Path('external/PolyChordLite/lib/libchord.so')
out={
 'q':'Q-042','program_id':'Q042-PROD-V17',
 'stage':'POLYCHORD_PARTIAL_INIT_RUNTIME_V17','status':'PASS',
 'scientific_result':False,'scientific_contract_changed':False,
 'base_commit':src['base_commit'],
 'checkpoint_interval':25,'serial_only':True,
 'patcher_sha256':'22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6',
 'selftest_sha256':'1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9',
 'selftest_status':st['status'],
 'selftest_exact_resume_byte_identity':st['exact_resume_byte_identity'],
 'selftest_capture_method':st['capture_method'],
 'selftest_capture_attempt_used':st['capture_attempt_used'],
 'selftest_resume_sha256':st['baseline_resume_sha256'],
 'generate_file':str(gen),'generate_sha256':sha(gen),
 'nested_sampling_file':str(nested),'nested_sampling_sha256':sha(nested),
 'libchord_file':str(lib),'libchord_sha256':sha(lib),
}
pathlib.Path('q042_runtime/q042_polychord_partial_init_v17.json').write_text(
 json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V17_PARTIAL_INIT_RUNTIME_GATE=PASS')
PYV17
