# Cleanup installation packages

Current locally prepared cleanup: [20261024-b99a5c7-v330](../docs/maintenance/cleanup/20261024-b99a5c7-v330/REPORT.md).
Read [installation and recovery](../docs/maintenance/cleanup/20261024-b99a5c7-v330/INSTALL.md) before applying its exact-base patch.

The existing [24f380b patch](Bubbleverse_cleanup_24f380b.patch) is a historical installation package. Its workflow `.github/workflows/apply-bubbleverse-cleanup.yml` still uses its original path and checksum. It is not this release's installer; do not use it to install the new package.

The independently uploaded root copy has been moved byte-for-byte to [history/root-copy/](history/root-copy/Bubbleverse_cleanup_24f380b.patch). Both distinct historical copies are retained. No workflow or scientific file was changed.
