# Q048 V141 ingestion — upload/apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `1362398c74950f66eb061fa73d3c41b078a7b863` (`main`)  
Status: **USER_UPLOAD_PENDING**

Upload all files in this delivery directory to the repository top level using their exact filenames.

Two files are immutable V141 source-recovery copies that were referenced by the V141 manifest but are not present as direct paths in the observed GitHub commit:
- `Q048_V141_RAW_V1.json` — SHA256 `1faa36e2d27ee237508917bee0944388f9a34e2aad4e9cfa173a940d42993017`
- `Q048_V141_OBSTRUCTION_DIAGNOSTIC_V1.json` — SHA256 `611a51ad961dd43cd0147dd24dabc360e87c89d2d47ef38eb7084f73365d832c`

Do not edit or rename those two source files. All `Q048_V141_INGESTION_*`, the cumulative `Q047_SAMLET_JOURNAL_Q048_V141_INGESTED_V1.md`, and the V142 task are new append-only/current-view artifacts.

Before upload, if `main` has moved beyond the observed base, preserve history and reconcile rather than overwriting newer state. V141 remains terminal obstruction; V140 remains the accepted current actual state.
