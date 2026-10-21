# Q048 V144 — upload/apply instructions

Repository base observed: `Morfindien/Bubbleverse main@4a067d08fc3d1f1b83620634bb275d771e283386`.

1. Upload the preceding V143 ingestion package first if it is not already in GitHub, because V144 authorization depends on `Q048_V143_INGESTION_STATE_V1.json` and the V144 task.
2. Upload every file listed in `Q048_V144_FILES_V1.md` as new files. Preserve the malformed V144 pre-freeze JSON files exactly as delivered; they are failure evidence.
3. Do **not** fix/overwrite any V144 frozen file in place and do not label V144 PASS.
4. After ingestion, a separately versioned V145 repair may correct the serializer and create new freeze/run artifacts.
