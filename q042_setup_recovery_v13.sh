#!/usr/bin/env bash
set -euo pipefail

# Recreate the frozen V1/V8 science runtime first.
bash q042_setup_recovery_v8.sh

# Apply the V13 serial-only partial GenerateLivePoints checkpoint patch.
python q042_patch_polychord_partial_init_v13.py \
  --root external/PolyChordLite \
  --manifest q042_runtime/q042_polychord_partial_init_source_v13.json

POLY="$PWD/external/PolyChordLite"
test "$(git -C "$POLY" rev-parse HEAD)" = "3ade6445bb3719a6db6f6e81f178765545ffc833"

# Rebuild the exact pinned release with the local technical patch.
# V12 proved that top-level `make clean || true` can leave lib/libchord.so in place,
# causing make to report "Nothing to be done" and execute the stale unpatched binary.
# Remove the library targets explicitly; patched source mtimes then force the dependent
# generate/nested_sampling objects to rebuild before relinking.
rm -f "$POLY/lib/libchord.so" "$POLY/lib/libchord.a"
make -C "$POLY/src/polychord" clean
make -C "$POLY" -e libchord.so MPI=1
test -s "$POLY/lib/libchord.so"

# Fail closed unless the linked binary itself contains the patch symbols.
NM_OUT="$(nm "$POLY/lib/libchord.so")"
grep -qi 'q042_write_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_WRITE_SYMBOL_GATE=FAIL'; exit 71; }
grep -qi 'q042_read_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_READ_SYMBOL_GATE=FAIL'; exit 72; }
grep -qi 'q042_delete_partial_init' <<<"$NM_OUT" || { echo 'Q042_PATCHED_BINARY_DELETE_SYMBOL_GATE=FAIL'; exit 73; }
echo 'Q042_POLYCHORD_PATCHED_BINARY_SYMBOL_GATE=PASS'

python -m pip install --disable-pip-version-check --force-reinstall --no-build-isolation --no-deps "$POLY"

# Fast deterministic technical test: uninterrupted vs interrupted+partial-resume
# must produce byte-identical final stock PolyChord resume state.
python q042_polychord_partial_init_selftest_v13.py \
  --output q042_runtime/q042_polychord_partial_init_selftest_v13.json

python - <<'PY'
import hashlib,json,pathlib
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

src=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_source_v13.json').read_text())
st=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_selftest_v13.json').read_text())
assert src['status']=='PASS'
assert src['base_commit']=='3ade6445bb3719a6db6f6e81f178765545ffc833'
assert src['checkpoint_interval']==25 and src['serial_only'] is True
assert st['status']=='PASS' and st['exact_resume_byte_identity'] is True

gen=pathlib.Path(src['generate_file'])
nested=pathlib.Path(src['nested_sampling_file'])
lib=pathlib.Path('external/PolyChordLite/lib/libchord.so')
out={
 'q':'Q-042','program_id':'Q042-PROD-V13',
 'stage':'POLYCHORD_PARTIAL_INIT_RUNTIME_V13','status':'PASS',
 'scientific_result':False,
 'base_commit':src['base_commit'],
 'checkpoint_interval':25,'serial_only':True,
 'patcher_sha256':'22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6',
 'selftest_sha256':'7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462',
 'selftest_status':st['status'],
 'selftest_exact_resume_byte_identity':st['exact_resume_byte_identity'],
 'selftest_resume_sha256':st['baseline_resume_sha256'],
 'generate_file':str(gen),'generate_sha256':sha(gen),
 'nested_sampling_file':str(nested),'nested_sampling_sha256':sha(nested),
 'libchord_file':str(lib),'libchord_sha256':sha(lib),
}
pathlib.Path('q042_runtime/q042_polychord_partial_init_v13.json').write_text(
 json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V13_PARTIAL_INIT_RUNTIME_GATE=PASS')
PY
