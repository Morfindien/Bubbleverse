# Q048 V140 upload/apply instructions

Base observed before V140 execution: `Morfindien/Bubbleverse@baa8bb567563bc513d2a509c10d8073408661204`. Re-check `main` before applying. Do not overwrite historical V139 or V138 artifacts.

Upload top-level memory/handoff files at repository root. Upload V140 runtime artifacts and source files under proposed `Q048_V140_RUNTIME/`. The complete cumulative journal is a new top-level version and preserves the V139-ingested journal byte-for-byte as prefix.

After upload, verify exact SHA-256 values against `Q048_V140_SHA256SUMS.txt`. Do not mark V140 synchronized until the resulting commit is observed. V139 must remain terminal FAIL; do not replace it with V140.
