# Q048 V142 ingestion — upload/apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `b7af5c062ab5d006069cbb73d634812a44b5e33f`  
Expected parent: `f7e78523efddd6530c70ede04971320d8853e831`

Upload all files in this package as new top-level records using the filenames shown. Do not overwrite historical V141/V142 science artifacts.

Two files are **recovery copies** of V142 artifacts omitted from commit `b7af5c062ab5d006069cbb73d634812a44b5e33f` and should also be added top-level if still absent:
- `Q048_V142_RESULT_STATE_V1.json`
- `Q048_V142_HANDOFF_TO_INGESTION_V1.json`

The ingestion registers V142 once and prepares, but does not execute, `Q048_V143_NEXT_BUILDER_TASK_CONDITIONAL_CONSUMER_840_830_V1.json`. Current remains actual124/frontier840 until V143 independently passes all acceptance/publication gates.

Before upload, verify repository HEAD has not advanced incompatibly. If it has, reconcile rather than overwrite.
