#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
EXPECTED_MUSE_SHA="4933ceb993ceb92e48b2191b8ccb1595d182bc4bc3862c1fbad61d5f82136e9b"
PREFETCH="$ROOT/external/q014_v6_spt_assets/muse_3g_like_march_2025.zip"
REAL_CURL="$(command -v curl)"

# V6 keeps q014_setup_v5.sh byte-for-byte as the scientific/software setup base.
# For SPT chains only, intercept its one LAMBDA MUSE curl and feed the exact
# pre-fetched source artifact instead. Every other curl delegates to real curl.
if [[ "$CHAIN" == spt_d1_* || "$CHAIN" == "all" ]]; then
  test -f "$PREFETCH" || { echo "Q014_MUSE_PREFETCH_GATE=FAIL missing $PREFETCH" >&2; exit 28; }
  ACTUAL="$(sha256sum "$PREFETCH" | awk '{print $1}')"
  test "$ACTUAL" = "$EXPECTED_MUSE_SHA" || {
    echo "Q014_MUSE_SOURCE_FREEZE_GATE=FAIL expected=$EXPECTED_MUSE_SHA actual=$ACTUAL" >&2; exit 41; }
  WRAP="$ROOT/.q014_v6_bin"
  rm -rf "$WRAP"; mkdir -p "$WRAP"
  cat > "$WRAP/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
is_muse=0; out=""; prev=""
for arg in "$@"; do
  [[ "$arg" == *"muse_3g_like_march_2025.zip"* ]] && is_muse=1
  if [[ "$prev" == "-o" ]]; then out="$arg"; fi
  prev="$arg"
done
if [[ "$is_muse" = 1 ]]; then
  [[ -n "$out" ]] || { echo "Q014_MUSE_CURL_INTERCEPT_GATE=FAIL no -o target" >&2; exit 42; }
  cp "$Q014_V6_MUSE_SOURCE" "$out"
  echo "Q014_MUSE_CURL_INTERCEPT_GATE=PASS $out"
  exit 0
fi
exec "$Q014_V6_REAL_CURL" "$@"
EOF
  chmod +x "$WRAP/curl"
  export Q014_V6_MUSE_SOURCE="$PREFETCH" Q014_V6_REAL_CURL="$REAL_CURL"
  PATH="$WRAP:$PATH" bash "$ROOT/q014_setup_v5.sh" "$CHAIN"
else
  bash "$ROOT/q014_setup_v5.sh" "$CHAIN"
fi

# V5 implementation reads q014_v5_source_runtime. Preserve it and also expose a
# V6-named copy for artifact/provenance inspection.
rm -rf q014_v6_source_runtime
cp -a q014_v5_source_runtime q014_v6_source_runtime
echo "Q014_V6_SETUP_REUSE_GATE=PASS chain=$CHAIN"
