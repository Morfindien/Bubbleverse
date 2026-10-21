# Q048 V139 — GitHub upload/apply instructions

Base observed before V139 freeze: `eafa8bbb6e51ead016e7a6962616ae0947663f86`. Recheck current `main` before applying.

Upload top-level handoff/state/journal/manifest/validation/checksum/index files under their delivered names. Upload all V139 runtime evidence and scripts listed as `Q048_V139_RUNTIME/...` in the output manifest into that runtime directory. Preserve all earlier V138/V137 files unchanged.

This is a **failure record**: do not update current actual to124/frontier840. V139 delta is zero. Keep V138 proof850→840 accepted and unconsumed. Result Ingestion must decide the next separately versioned task.

No GitHub push/PR is claimed by this local run.
