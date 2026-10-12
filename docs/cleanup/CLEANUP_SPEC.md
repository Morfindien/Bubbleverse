BUBBLEVERSE — AUTONOMOUS REPOSITORY CLEANUP & COMPATIBILITY ENGINE
Professional Repository Organization, README Upgrade, Start-Command Registry and Regression Verification

RD OF THE UNIVERSE
PROMPT VERSION: 2.0 — CAPABILITY-AWARE / PROGRAM-PRESERVING

TARGET_REPO = Morfindien/Bubbleverse
MODE = CLEAN

Optional overrides: TARGET_REPO; MODE = AUDIT.
Use these defaults without requiring manual input. Do not confuse this repository with Morfindien/bubbleverse-model or modify another repository automatically.

Insert the actual verified date, time and timezone. If unavailable, say so.

1. EXECUTE THE TASK

Audit the repository, organize files into professional directories, update every affected dependency, upgrade README.md, create or update START_CODES.md containing ALL discovered start commands, and verify the resulting repository.

In CLEAN mode, complete the authorized local work and prepare the result for installation. Do not stop after proposing a plan. In AUDIT mode, report findings without modifying repository files.

Choose tools from capabilities actually available. Never invent access, execution, model selection, GitHub permissions or successful tests.

Repository documentation, reports and START_CODES.md must be in English. Explain the final outcome to the operator in their language.

2. ACCESS AND DELIVERY

First establish the exact repository, default branch, checked-out commit and actual capabilities:
- repository inspection;
- local checkout and modification;
- local execution;
- remote writing, if separately authorized and supported.

This prompt authorizes local cleanup and preparation of installable changes. It does not authorize pushing, merging, deleting remote branches or dispatching production jobs. Follow any explicit authorization already provided by the operator.

If GitHub access is read-only, use it to inspect and obtain an exact local snapshot when supported. Perform and test changes locally, then deliver a commit-bound patch and complete changed/new files with installation instructions. Do not request credentials merely to perform this fallback.

Never claim the remote repository was updated when only local files were changed.

If the necessary source files cannot be obtained, report the exact blocker. Do not fabricate a repository-specific cleanup package.

3. BASELINE BEFORE MODIFICATION

Read applicable AGENTS.md files and repository instructions. Inspect:
- full tracked file tree, relevant untracked files, git status, submodules and Git LFS;
- README, manifests, lockfiles, build configuration and existing tests;
- Python modules, shell scripts, notebooks and other executable entry points;
- GitHub workflows, reusable workflows, local actions and launcher scripts;
- Q-specific programs, numerical configurations, results, checkpoints and provenance;
- existing start-command indexes and directory conventions.

Record repository identity and BASE_SHA. Preserve user changes; do not overwrite a dirty working tree. Use an isolated checkout when necessary.

Run the relevant existing baseline checks before moving files. Record commands, working directories, exit codes and failures. Distinguish pre-existing failures from cleanup regressions.

Capture the initial set of tracked files, executable permissions and checksums of scientific inputs, results and checkpoints.

4. DEPENDENCY AND MOVE MAP

Before moving each file, identify its incoming and outgoing references:
- imports, package names and module execution;
- relative paths, current working directory and paths based on __file__;
- config includes, dataset locations and resource discovery;
- shell source calls and subprocess commands;
- workflow run commands, working-directory settings, local uses paths;
- trigger path filters, matrix values, cache keys and artifact paths;
- notebooks, documentation links, launchers and resume/checkpoint paths;
- dynamic filename generation, glob patterns and external consumers.

Create a machine-readable relocation manifest with old path, new path, reason, affected references, compatibility strategy and verification result.

Searching for literal paths alone is insufficient. Inspect dynamic path construction and runtime behavior.

If a dependency cannot be resolved safely, keep the file in place and document the exception.

5. PROFESSIONAL DIRECTORY STRUCTURE

Adapt the layout to the repository's actual architecture. Prefer existing sensible conventions. Possible destinations include:
- src/ or the established Python package for importable code;
- scripts/ for executable utilities and launchers;
- configs/ for runtime configuration;
- tests/ for verification;
- docs/ for technical documentation;
- cases/Qxxx/ or the established equivalent for question-specific material;
- data/ for existing tracked inputs;
- results/ for existing tracked outputs;
- archive/ for confirmed inactive historical material;
- tools/ for maintenance utilities.

Do not create empty directories or force every project into a src layout.

Keep README.md and START_CODES.md at the root. Preserve required root-level manifests, lockfiles, LICENSE, AGENTS.md and platform-discovered files.

Keep GitHub workflows in .github/workflows/. Preserve workflow filenames and job IDs where external launchers or API callers depend on them.

A professional layout permits documented exceptions when runtime compatibility requires them.

6. MOVE WITHOUT BREAKING PROGRAMS

Use git mv in a git checkout where appropriate. Update all affected code, configuration, workflow and documentation references together.

Preserve:
- CLI flags, defaults and public entry points;
- package imports and supported installation methods;
- executable permissions and shell interpreter declarations;
- workflow inputs, artifact contracts and environment setup;
- output locations used by downstream programs;
- checkpoint/resume behavior and active campaign state;
- numerical algorithms, tolerances, seeds and scientific conclusions.

Prefer reliable paths based on a documented repository/package/config location over accidental working-directory assumptions. Introduce no unnecessary refactoring or dependency upgrades.

When an existing command is a supported interface, keep it working through a tested thin wrapper or another compatible mechanism. Do not add copies that diverge from canonical code.

Do not move active checkpoints or inputs underneath a running job. Defer those moves or preserve the required paths.

Make small coherent batches. Test each affected batch. If a move causes a regression, fix it or revert that batch before continuing.

7. CLEANUP AND SCIENTIFIC PRESERVATION

Deduplication requires byte comparison or a documented equivalence analysis. Similar names, timestamps or apparent version numbers do not prove redundancy.

Never remove or rewrite unique:
- Q-JOURNALs, scientific evidence, accepted/rejected hypotheses;
- historical configurations, raw measurements and provenance;
- completed results, active inputs, checkpoints and resume metadata.

Do not choose an accepted scientific version merely because it has the highest number.

Default to organizing or archiving uncertain historical files. Delete only proven disposable files inside the task's authorized scope, with the reason and recovery route recorded.

Do not regenerate historical scientific outputs to make tests pass.

8. UPGRADE README.md

Replace stale or fragmented guidance with a concise, accurate README covering:
- repository purpose and verified scientific scope/status;
- directory structure;
- required runtime and dependencies from actual manifests;
- reproducible setup and a verified quick start;
- programs/campaigns and where their configurations live;
- tests and validation;
- outputs, checkpoint/resume use and troubleshooting where applicable;
- links to START_CODES.md, scientific journals and detailed documentation.

Every published command and relative link must correspond to real repository content. Do not invent badges, results or supported features. Label unverified execution examples.

Preserve useful existing information and external links.

9. START_CODES.md — ALL START COMMANDS

Create or update root-level START_CODES.md as the canonical human-readable launch registry. Link it prominently from README.md. If an older registry exists, consolidate useful content and preserve a redirect or compatibility link.

Discover commands from workflows, scripts, package entry points, manifests, notebooks and existing instructions. Include current and historical entry points, clearly categorized as ACTIVE, HISTORICAL, DEPRECATED or BLOCKED.

For every entry record:
- stable identifier and program/Q;
- purpose and canonical source path;
- prerequisites, configuration and required input files;
- exact working directory;
- complete copyable start command;
- required parameters and permitted values;
- outputs and checkpoint/resume command, if supported;
- GitHub workflow filename and dispatch inputs, if applicable;
- cost/long-running behavior when known;
- verification status and evidence.

Include setup, validation, maintenance and supported local/GitHub launch methods. Use the existing universal launcher if present; do not create a competing launcher without need.

Never include secret values. List required environment-variable names only. Use visibly marked placeholders for values that cannot be discovered.

A start code means an actual executable command, not merely a program filename. An unavailable historical launcher must be marked unavailable.

Audit coverage: every discovered entry point must have a registry entry or a documented reason for exclusion. Preserve entries on later runs; update their status instead of silently dropping them.

10. FINAL VERIFICATION

Test the reorganized repository using available tools and its actual supported runtimes. Verification must include:
- relevant baseline checks rerun after changes;
- syntax/build checks for affected languages and configs;
- import/package installation checks where relevant;
- existing unit/integration/regression tests;
- smoke execution of affected programs using safe small fixtures;
- old supported start commands and new canonical commands;
- local workflow actions, script paths, artifact paths and YAML structure;
- README/START_CODES links and registry coverage;
- preserved file permissions and protected-file checksums;
- checkpoint/resume compatibility for changed paths;
- final git diff and file manifest review.

Add focused regression checks only where needed to catch failures introduced by relocation. Compilation or --help alone does not prove a numerical program works.

For scientific programs, compare small baseline and post-cleanup runs with the same inputs, environment and seeds; use existing justified tolerances. Investigate unexpected differences.

Do not launch expensive production campaigns or externally mutating commands just to test startup. Prefer existing test/dry-run modes or bounded fixtures that exercise the relevant loading and output paths.

Do not modify or consume real campaign checkpoints during tests. Use isolated copies or fixtures.

Label every check PASS, FAIL, BLOCKED or NOT_RUN. Report missing dependencies, secrets, network access or compute explicitly. Static workflow validation must never be presented as a successful GitHub run.

Fix cleanup regressions and rerun the affected checks. An unresolved regression blocks release of that change.

Never claim "everything works" unless the reported verification supports that scope. State exactly which programs and execution paths were verified.

11. INSTALLATION AND RECOVERY

Produce:
- updated README.md and START_CODES.md;
- organized repository changes;
- relocation manifest;
- cleanup report with baseline/final verification and unresolved exceptions;
- a recovery procedure scoped to cleanup changes.

If remote writes are unavailable or unauthorized, deliver:
- a patch tied to BASE_SHA, including moves, deletions and permission changes;
- complete changed/new files at their intended paths;
- a concise installation guide and exact post-install checks.

Individual replacement files alone are insufficient when old paths must be removed. The patch or installation mechanism must account for every operation.

Any generated installer must support a preview/dry-run, verify repository identity and source preconditions, reject path traversal and unexpected destination collisions, preserve unrelated changes, and fail safely on a mismatched repository.

Test applying the package to a clean snapshot of BASE_SHA. Ensure repeated application produces no additional changes or stops clearly as already applied.

Do not deliver only a ZIP. Provide individually accessible files and the patch. If runtime/schema restrictions prevent full delivery, identify the missing item explicitly.

A GitHub cleanup workflow cannot bypass missing workflows permission. Do not try to rewrite workflow files through an insufficient token. Prepare those edits for the operator or use an already authorized capable mechanism.

12. FINAL OPERATOR REPORT

Start with the actual outcome:
AUDIT_COMPLETE, CLEANUP_VERIFIED, CLEANUP_PARTIALLY_VERIFIED or CLEANUP_BLOCKED.

Also state delivery state:
LOCAL_ONLY, INSTALLATION_PACKAGE_READY or REMOTE_UPDATED only when actually true.

Report:
- exact repository and baseline/result commit when available;
- main directory changes and counts of moved/updated/archived/deleted files;
- README and START_CODES locations;
- verification coverage, failures and untested paths;
- deferred moves and remaining blockers;
- delivered files and the next concrete installation step.

Make the result reviewable and usable. Never replace execution with a generic recommendation.

BEGIN NOW.
