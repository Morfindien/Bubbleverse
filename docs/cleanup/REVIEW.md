# Independent review and resolution

A separate read-only reviewer checked the staged cleanup against BASE_SHA, the supplied spec and the local verification evidence. It independently confirmed all 96 archive byte/mode matches and all 73 canonical root aliases. Three findings were resolved before delivery:

1. Root README omitted the historical reconstruction identity required by its static repository gate. The actual `python q047_reconstruction_v1.py static --program-id Q047-RECONSTRUCTION-V1` command passed baseline, failed before correction, then passed after historical root context was retained. The Q048 README pin was updated together.
2. Thirty top-level README/registry patch scripts were wrongly labeled import-only. They now have explicit BLOCKED historical executable commands, warnings and CLI schemas. A new fixture failed before the coverage gate change and passed after.
3. The layout checker did not enforce the README-only lock exception. It now verifies the preserved original lock SHA, compares every other JSON field and checks the live README digest. Two adversarial fixtures failed before implementation and pass afterward.

The full new fixture suite is twelve tests, all PASS. The selected 68 historical Q047/Q048 tests retain exactly their three baseline defects and one native-header skip. No deferred review finding remains. Full numerical production and live checkpoint qualification remain outside verified scope.

Installation testing discovered a Git stat-cache issue after restoring identical README bytes. Refreshing clean-file index metadata fixes this without overwriting content; affected changes/collisions are still rejected by git apply --index. Thirteen integration checks pass, including preview, wrong repository/HEAD rejection, collisions, unrelated staged work, three installed runtime gates, repeat application, overlapping-edit rejection, reversal and checksum tampering.
