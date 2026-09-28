#!/usr/bin/env bash
set -euo pipefail

# Recreate the frozen V1/V8 science runtime first.
bash q042_setup_recovery_v8.sh

# Apply the V11 serial-only partial GenerateLivePoints checkpoint patch.
python q042_patch_polychord_partial_init_v11.py \
  --root external/PolyChordLite \
  --manifest q042_runtime/q042_polychord_partial_init_source_v11.json

POLY="$PWD/external/PolyChordLite"
test "$(git -C "$POLY" rev-parse HEAD)" = "3ade6445bb3719a6db6f6e81f178765545ffc833"

# Rebuild the exact pinned release with the local technical patch.
make -C "$POLY" clean >/dev/null 2>&1 || true
make -C "$POLY" -e libchord.so MPI=1
test -s "$POLY/lib/libchord.so"
python -m pip install --disable-pip-version-check --force-reinstall --no-build-isolation --no-deps "$POLY"

# Fast deterministic technical test: uninterrupted vs interrupted+partial-resume
# must produce byte-identical final stock PolyChord resume state.
python q042_polychord_partial_init_selftest_v11.py \
  --output q042_runtime/q042_polychord_partial_init_selftest_v11.json

python - <<'PY'
import hashlib,json,pathlib
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

src=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_source_v11.json').read_text())
st=json.loads(pathlib.Path('q042_runtime/q042_polychord_partial_init_selftest_v11.json').read_text())
assert src['status']=='PASS'
assert src['base_commit']=='3ade6445bb3719a6db6f6e81f178765545ffc833'
assert src['checkpoint_interval']==25 and src['serial_only'] is True
assert st['status']=='PASS' and st['exact_resume_byte_identity'] is True

gen=pathlib.Path(src['generate_file'])
nested=pathlib.Path(src['nested_sampling_file'])
lib=pathlib.Path('external/PolyChordLite/lib/libchord.so')
out={
 'q':'Q-042','program_id':'Q042-PROD-V11',
 'stage':'POLYCHORD_PARTIAL_INIT_RUNTIME_V11','status':'PASS',
 'scientific_result':False,
 'base_commit':src['base_commit'],
 'checkpoint_interval':25,'serial_only':True,
 'patcher_sha256':'b8dc1fe134f69068fb5a1c97044b4bb5910b93320156acae009b76135a3f9136',
 'selftest_sha256':'7f103dd2fd7a6f5575af4de43e8102d3b99893abaf16ee2ea1973a8780de7a69',
 'selftest_status':st['status'],
 'selftest_exact_resume_byte_identity':st['exact_resume_byte_identity'],
 'selftest_resume_sha256':st['baseline_resume_sha256'],
 'generate_file':str(gen),'generate_sha256':sha(gen),
 'nested_sampling_file':str(nested),'nested_sampling_sha256':sha(nested),
 'libchord_file':str(lib),'libchord_sha256':sha(lib),
}
pathlib.Path('q042_runtime/q042_polychord_partial_init_v11.json').write_text(
 json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q042_PROD_V11_PARTIAL_INIT_RUNTIME_GATE=PASS')
PY
