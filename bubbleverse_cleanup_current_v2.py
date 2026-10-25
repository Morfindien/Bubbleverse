#!/usr/bin/env python3
"""
Bubbleverse current-state repository cleanup engine.

Target: Morfindien/Bubbleverse
Design:
- never rewrites scientific journals/results to make the tree prettier;
- archives only registry-backed retired program/workflow pairs with explicit retirement evidence;
- refuses moves when an active registry entry or an unresolved incoming reference still depends on a path;
- generates START_CODES.md, repository structure documentation, cleanup evidence and machine-readable manifests;
- stages changes locally; publication is handled by the companion GitHub Actions workflow.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

REPOSITORY = "Morfindien/Bubbleverse"
PROMPT_ID = "BV-REPOSITORY-CLEANUP"
PROMPT_VERSION = "3.3.0"
ENGINE_VERSION = "current-v2"
REGISTRY_PATH = Path("bubbleverse_program_registry.json")
README_PATH = Path("README.md")
START_CODES_PATH = Path("START_CODES.md")
STRUCTURE_PATH = Path("docs/REPOSITORY_STRUCTURE.md")
CLEANUP_INDEX_PATH = Path("docs/maintenance/cleanup/INDEX.md")
ARCHIVE_INDEX_PATH = Path("archive/programs/INDEX.md")
MANAGED_README_START = "<!-- BV-CLEANUP-CURRENT-V2:START -->"
MANAGED_README_END = "<!-- BV-CLEANUP-CURRENT-V2:END -->"

# Retirement evidence accepted automatically by this engine.
# COMPLETED alone is intentionally NOT enough.
def has_retirement_evidence(rec: dict[str, Any]) -> tuple[bool, str]:
    status = str(rec.get("status", "")).upper()
    superseded_by = rec.get("superseded_by")
    if status == "SUPERSEDED":
        return True, "registry status SUPERSEDED"
    if status in {"BROKEN", "FAILED"} and superseded_by:
        return True, f"registry status {status} with superseded_by={superseded_by}"
    if status == "COMPLETED_HISTORICAL" and rec.get("superseded_by"):
        return True, f"registry status COMPLETED_HISTORICAL with superseded_by={rec.get('superseded_by')}"
    return False, f"retirement not proven by registry (status={status or 'UNKNOWN'})"


def run(args: list[str], root: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        args,
        cwd=root,
        text=True,
        capture_output=True,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
    )
    if check and cp.returncode:
        raise RuntimeError(
            "Command failed: " + " ".join(args) + "\nSTDOUT:\n" + cp.stdout + "\nSTDERR:\n" + cp.stderr
        )
    return cp


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_rel(value: str) -> str:
    p = PurePosixPath(value)
    need(bool(value), "Empty path")
    need(not p.is_absolute(), f"Absolute path not allowed: {value}")
    need(".." not in p.parts, f"Path traversal not allowed: {value}")
    need("\\" not in value, f"Backslash path not allowed: {value}")
    return value


def tracked_files(root: Path) -> list[str]:
    cp = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return [p.decode("utf-8") for p in cp.stdout.split(b"\0") if p]


def blob_info(root: Path, rel: str) -> dict[str, Any]:
    p = root / rel
    st = p.lstat()
    is_symlink = stat.S_ISLNK(st.st_mode)
    info: dict[str, Any] = {
        "path": rel,
        "size": st.st_size,
        "mode": oct(stat.S_IMODE(st.st_mode)),
        "is_symlink": is_symlink,
        "symlink_target": os.readlink(p) if is_symlink else None,
        "sha256": None if is_symlink else sha256_file(p),
    }
    return info


def load_registry(root: Path) -> dict[str, Any]:
    p = root / REGISTRY_PATH
    need(p.is_file(), f"Missing {REGISTRY_PATH}")
    obj = json.loads(p.read_text(encoding="utf-8"))
    need(isinstance(obj, dict) and isinstance(obj.get("programs"), dict), "Unsupported program registry schema")
    return obj


def records_by_path(programs: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    refs: dict[str, set[str]] = defaultdict(set)
    for rid, rec in programs.items():
        for key in ("workflow_path", "scientific_program", "tests", "preregister", "source_lock"):
            v = rec.get(key)
            if isinstance(v, str) and v:
                refs[v].add(rid)
    return refs


def active_paths(programs: dict[str, dict[str, Any]]) -> set[str]:
    out: set[str] = set()
    for _, rec in programs.items():
        if str(rec.get("status", "")).upper() != "ACTIVE":
            continue
        for key in ("workflow_path", "scientific_program", "tests", "preregister", "source_lock"):
            v = rec.get(key)
            if isinstance(v, str) and v:
                out.add(v)
    return out


def candidate_retired_payloads(programs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Return only workflow/program paths backed by explicit retirement evidence.
    Supporting scientific data, journals, results, preregisters, source locks and tests
    are intentionally NOT auto-moved by this engine.
    """
    out: dict[str, dict[str, Any]] = {}
    for rid, rec in programs.items():
        ok, evidence = has_retirement_evidence(rec)
        if not ok:
            continue
        q = str(rec.get("q") or "UNKNOWN").replace("-", "")
        for kind, key in (("workflow", "workflow_path"), ("program", "scientific_program")):
            v = rec.get(key)
            if isinstance(v, str) and v:
                out[v] = {
                    "record_id": rid,
                    "record": rec,
                    "q": q,
                    "kind": kind,
                    "evidence": evidence,
                }
    return out


def text_grep_references(root: Path, rel: str, ignore: set[str]) -> list[str]:
    """
    Conservative exact literal path search. If a path is referenced by a tracked text file
    outside the allowed metadata/navigation set, the archive move is deferred.
    """
    cp = run(["git", "grep", "-l", "-F", "--", rel], root, check=False)
    if cp.returncode not in (0, 1):
        raise RuntimeError(f"git grep failed for {rel}: {cp.stderr}")
    refs = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    return sorted(r for r in refs if r not in ignore and r != rel)


def sanitize_segment(v: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", v).strip("-")
    return s or "UNKNOWN"


def destination_for(meta: dict[str, Any], rel: str) -> str:
    rid = sanitize_segment(meta["record_id"])
    q = sanitize_segment(meta["q"])
    leaf = PurePosixPath(rel)
    return str(
        PurePosixPath("archive/programs")
        / q
        / rid
        / "registry-retired"
        / "payload"
        / leaf
    )


def make_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj: Any) -> None:
    make_parent(path)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def move_with_git(root: Path, old: str, new: str) -> None:
    safe_rel(old)
    safe_rel(new)
    src = root / old
    dst = root / new
    need(src.exists() or src.is_symlink(), f"Source missing: {old}")
    need(not dst.exists(), f"Destination collision: {new}")
    make_parent(dst)
    run(["git", "mv", "--", old, new], root)


def upsert_managed_block(text: str, block: str) -> str:
    if MANAGED_README_START in text and MANAGED_README_END in text:
        a = text.index(MANAGED_README_START)
        b = text.index(MANAGED_README_END, a) + len(MANAGED_README_END)
        return text[:a] + block + text[b:]
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block + "\n"


def workflow_names(files: list[str]) -> list[str]:
    return sorted(
        p for p in files
        if p.startswith(".github/workflows/") and p.lower().endswith((".yml", ".yaml"))
    )


def render_start_codes(programs: dict[str, dict[str, Any]], files_after: list[str]) -> str:
    lines = [
        "# START_CODES",
        "",
        "Canonical launch registry for the Bubbleverse repository.",
        "",
        "> Lifecycle describes repository/program status. Verification of a command must be established by its own run evidence.",
        "",
        "## Repository maintenance",
        "",
        "```bash",
        "gh workflow run apply-bubbleverse-cleanup-current-v2.yml --repo Morfindien/Bubbleverse --ref main -f mode=preview",
        "gh workflow run apply-bubbleverse-cleanup-current-v2.yml --repo Morfindien/Bubbleverse --ref main -f mode=apply",
        "```",
        "",
        "## Registry-backed scientific programs",
        "",
    ]
    for rid in sorted(programs):
        rec = programs[rid]
        status = str(rec.get("status", "UNKNOWN"))
        program = rec.get("scientific_program")
        workflow = rec.get("workflow_path")
        archive_program = rec.get("cleanup_archive_program_path")
        archive_workflow = rec.get("cleanup_archive_workflow_path")
        lines += [f"### {rid} — {status}", ""]
        if archive_program or archive_workflow:
            lines.append("Lifecycle: **ARCHIVED / reference only**")
            if archive_program:
                lines.append(f"- Archived program: `{archive_program}`")
            if archive_workflow:
                lines.append(f"- Archived workflow: `{archive_workflow}`")
            if program:
                lines.append(f"- Historical program path: `{program}`")
            if workflow:
                lines.append(f"- Historical workflow path: `{workflow}`")
            lines += ["- Execution: **NOT_RUN — RETIRED_PROGRAM**", ""]
            continue
        lines.append(f"Lifecycle: **{status}**")
        if isinstance(workflow, str) and workflow in files_after:
            wf = PurePosixPath(workflow).name
            lines += [
                f"- Workflow: `{workflow}`",
                "",
                "```bash",
                f"gh workflow run {wf} --repo Morfindien/Bubbleverse --ref main",
                "```",
            ]
        elif workflow:
            lines.append(f"- Workflow: `{workflow}` (not present at active path)")
        if isinstance(program, str) and program in files_after:
            lines += [
                f"- Program: `{program}`",
                "",
                "```bash",
                f"python {program}",
                "```",
            ]
        elif program:
            lines.append(f"- Program: `{program}` (not present at active path)")
        lines.append("")
    # Also expose workflow files not represented in the program registry.
    registered = {
        rec.get("workflow_path")
        for rec in programs.values()
        if isinstance(rec.get("workflow_path"), str)
    }
    extra = [p for p in workflow_names(files_after) if p not in registered]
    lines += ["## Other active workflow files discovered", ""]
    for p in extra:
        wf = PurePosixPath(p).name
        lines += [
            f"### {wf}",
            "",
            f"Source: `{p}`",
            "",
            "```bash",
            f"gh workflow run {wf} --repo Morfindien/Bubbleverse --ref main",
            "```",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def render_structure(counts: Counter[str], root_count: int, archive_count: int, deferred: int) -> str:
    lines = [
        "# Repository Structure",
        "",
        "Generated by the Bubbleverse current-state cleanup engine.",
        "",
        "## Canonical locations",
        "",
        "- `README.md` — public repository entry point.",
        "- `START_CODES.md` — canonical human-readable launch registry.",
        "- `.github/workflows/` — active GitHub Actions workflows only; registry-proven retired workflows may be archived.",
        "- `archive/programs/` — byte-preserving retired program/workflow bundles with archive metadata.",
        "- `docs/maintenance/cleanup/` — cleanup run records, manifests and validation evidence.",
        "- `docs/REPOSITORY_STRUCTURE.md` — this map.",
        "",
        "## Current tracked-file distribution",
        "",
    ]
    for key, value in counts.most_common():
        lines.append(f"- `{key}`: {value} files")
    lines += [
        "",
        f"Root-level tracked files: **{root_count}**.",
        f"Archived payload files created by this run: **{archive_count}**.",
        f"Retirement candidates deferred by safety gates: **{deferred}**.",
        "",
        "## Protected-history rule",
        "",
        "Scientific journals, historical results, inputs, provenance records and ambiguous historical code remain at their original paths unless a documented migration rule and retirement evidence permit a byte-preserving archive move.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    root = Path(run(["git", "rev-parse", "--show-toplevel"], Path.cwd()).stdout.strip()).resolve()
    need(root == Path.cwd().resolve(), "Run from repository root")
    need(os.environ.get("GITHUB_REPOSITORY", REPOSITORY) == REPOSITORY, f"Wrong repository; expected {REPOSITORY}")

    mode = os.environ.get("CLEANUP_MODE", "preview")
    need(mode in {"preview", "apply"}, "CLEANUP_MODE must be preview or apply")

    # We refuse to operate on a dirty checkout. GitHub Actions checkout is clean.
    need(run(["git", "diff", "--exit-code"], root, check=False).returncode == 0, "Dirty unstaged working tree")
    need(run(["git", "diff", "--cached", "--exit-code"], root, check=False).returncode == 0, "Dirty staged working tree")

    base_sha = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
    started = datetime.now(timezone.utc)
    run_id = f"{started.strftime('%Y%m%dT%H%M%SZ')}-{base_sha[:12]}-{ENGINE_VERSION}"
    run_dir = Path("docs/maintenance/cleanup") / run_id

    before = tracked_files(root)
    before_set = set(before)
    root_before = sorted(p for p in before if "/" not in p)

    registry = load_registry(root)
    programs: dict[str, dict[str, Any]] = registry["programs"]
    path_records = records_by_path(programs)
    active = active_paths(programs)
    candidates = candidate_retired_payloads(programs)

    placement: list[dict[str, Any]] = []
    operations: list[dict[str, Any]] = []
    validation: list[dict[str, Any]] = []
    protected_inventory: list[dict[str, Any]] = []
    archived_by_record: dict[str, list[dict[str, str]]] = defaultdict(list)

    candidate_decision: dict[str, tuple[str, str, str | None]] = {}

    # Determine safe archive moves.
    for rel, meta in sorted(candidates.items()):
        if rel not in before_set:
            candidate_decision[rel] = ("DEFER_BLOCKED", "registry path is absent from tracked checkout", None)
            continue
        if rel in active:
            candidate_decision[rel] = ("DEFER_BLOCKED", "path is also referenced by an ACTIVE registry entry", None)
            continue
        refs = path_records.get(rel, set())
        if len(refs) != 1 or meta["record_id"] not in refs:
            candidate_decision[rel] = (
                "DEFER_BLOCKED",
                f"path is shared by multiple registry records: {sorted(refs)}",
                None,
            )
            continue
        ignored = {
            str(REGISTRY_PATH),
            str(START_CODES_PATH),
            str(STRUCTURE_PATH),
            str(CLEANUP_INDEX_PATH),
        }
        incoming = text_grep_references(root, rel, ignored)
        # References from the companion program/workflow of the same retired record are allowed.
        companion = {
            str(meta["record"].get("workflow_path") or ""),
            str(meta["record"].get("scientific_program") or ""),
        }
        incoming = [x for x in incoming if x not in companion]
        if incoming:
            candidate_decision[rel] = (
                "DEFER_BLOCKED",
                "unresolved incoming literal references: " + ", ".join(incoming[:8]),
                None,
            )
            continue
        dest = destination_for(meta, rel)
        candidate_decision[rel] = ("ARCHIVE_RETIRED", meta["evidence"], dest)

    # Inventory and placement decision for every tracked file.
    for rel in before:
        if rel in candidate_decision:
            decision, reason, dest = candidate_decision[rel]
            placement.append(
                {
                    "path": rel,
                    "placement_decision": decision,
                    "target_path": dest,
                    "decision_reason": reason,
                }
            )
            if decision != "ARCHIVE_RETIRED":
                protected_inventory.append({**blob_info(root, rel), "protection_reason": reason})
            continue

        if "/" not in rel:
            if rel in {"README.md", "START_CODES.md", "LICENSE", "LICENSE.md", "pyproject.toml", "requirements.txt"}:
                decision = "KEEP_REQUIRED_ROOT"
                reason = "root interface/platform file"
            else:
                decision = "KEEP_PROTECTED"
                reason = "root historical/scientific/support file not proven movable by current evidence"
                protected_inventory.append({**blob_info(root, rel), "protection_reason": reason})
        else:
            decision = "KEEP_CORRECT_LOCATION"
            reason = "existing nested location retained; no verified safe relocation required"
        placement.append(
            {
                "path": rel,
                "placement_decision": decision,
                "target_path": None,
                "decision_reason": reason,
            }
        )

    # Apply archive moves only after the whole decision map is known.
    for rel, (decision, reason, dest) in sorted(candidate_decision.items()):
        if decision != "ARCHIVE_RETIRED" or not dest:
            continue
        src_info = blob_info(root, rel)
        meta = candidates[rel]
        move_with_git(root, rel, dest)
        dst_info = blob_info(root, dest)
        need(src_info["sha256"] == dst_info["sha256"], f"Byte mismatch after move: {rel}")
        operations.append(
            {
                "operation_id": "ARCHIVE-" + hashlib.sha256(rel.encode()).hexdigest()[:16],
                "operation": "ARCHIVE",
                "old_path": rel,
                "new_path": dest,
                "record_id": meta["record_id"],
                "kind": meta["kind"],
                "reason": reason,
                "source_sha256": src_info["sha256"],
                "destination_sha256": dst_info["sha256"],
                "verification": "PASS",
                "recovery": f"git mv -- {dest} {rel}",
            }
        )
        archived_by_record[meta["record_id"]].append(
            {"kind": meta["kind"], "old_path": rel, "new_path": dest, "sha256": src_info["sha256"]}
        )
        rec = programs[meta["record_id"]]
        if meta["kind"] == "workflow":
            rec["cleanup_archive_workflow_path"] = dest
        else:
            rec["cleanup_archive_program_path"] = dest
        rec["cleanup_execution_lifecycle"] = "ARCHIVED"
        rec["cleanup_retirement_evidence"] = reason
        rec["cleanup_run_id"] = run_id

    # Add archive metadata for bundles.
    for rid, moved in archived_by_record.items():
        rec = programs[rid]
        q = sanitize_segment(str(rec.get("q") or "UNKNOWN").replace("-", ""))
        bundle = Path("archive/programs") / q / sanitize_segment(rid) / "registry-retired"
        info = [
            "# ARCHIVE_INFO",
            "",
            "**ARCHIVED — NOT FOR ROUTINE EXECUTION**",
            "",
            f"- Registry record: `{rid}`",
            f"- Scientific Q: `{rec.get('q', 'UNKNOWN')}`",
            f"- Registry scientific status: `{rec.get('status', 'UNKNOWN')}`",
            f"- Cleanup run: `{run_id}`",
            f"- Source commit: `{base_sha}`",
            f"- Retirement evidence: {rec.get('cleanup_retirement_evidence')}",
            "",
            "## Moved payload",
            "",
        ]
        for item in moved:
            info += [
                f"- `{item['old_path']}` → `{item['new_path']}`",
                f"  - SHA-256: `{item['sha256']}`",
            ]
        info += [
            "",
            "Historical scientific results, journals, datasets and provenance records were not moved by this archive operation.",
            "",
            "Recovery uses the recorded inverse `git mv` operations in the cleanup relocation manifest.",
            "",
        ]
        make_parent(root / bundle / "ARCHIVE_INFO.md")
        (root / bundle / "ARCHIVE_INFO.md").write_text("\n".join(info), encoding="utf-8")

    # Persist registry additions only if archives were actually created.
    if archived_by_record:
        write_json(root / REGISTRY_PATH, registry)

    # Generate launch registry after moves.
    after_moves = tracked_files(root)
    start_text = render_start_codes(programs, after_moves)
    START_CODES_PATH.write_text(start_text, encoding="utf-8")

    # Documentation and indexes.
    top_counts = Counter(p.split("/", 1)[0] if "/" in p else "<ROOT>" for p in tracked_files(root))
    deferred_count = sum(1 for d, _, _ in candidate_decision.values() if d == "DEFER_BLOCKED")
    STRUCTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STRUCTURE_PATH.write_text(
        render_structure(top_counts, len(root_before), len(operations), deferred_count),
        encoding="utf-8",
    )

    # Update README only through a managed navigation block.
    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Bubbleverse\n"
    managed = "\n".join(
        [
            MANAGED_README_START,
            "## Repository navigation",
            "",
            "- [START_CODES.md](START_CODES.md) — canonical launch registry.",
            "- [Repository structure](docs/REPOSITORY_STRUCTURE.md).",
            "- [Cleanup history](docs/maintenance/cleanup/INDEX.md).",
            "- [Retired program archive](archive/programs/INDEX.md).",
            "",
            "Historical scientific records remain authoritative at their preserved source locations unless a documented byte-preserving archive mapping says otherwise.",
            MANAGED_README_END,
        ]
    )
    README_PATH.write_text(upsert_managed_block(readme, managed), encoding="utf-8")

    # Archive index.
    archive_lines = [
        "# Retired Program Archive",
        "",
        "This index lists program/workflow bundles archived by repository maintenance.",
        "Archived code is reference-only and is intentionally outside active GitHub workflow discovery.",
        "",
    ]
    if archived_by_record:
        for rid in sorted(archived_by_record):
            rec = programs[rid]
            q = sanitize_segment(str(rec.get("q") or "UNKNOWN").replace("-", ""))
            bundle = f"{q}/{sanitize_segment(rid)}/registry-retired/ARCHIVE_INFO.md"
            archive_lines.append(f"- [{rid}]({bundle}) — {rec.get('cleanup_retirement_evidence')}")
    else:
        archive_lines.append("- No registry-proven bundles were archived by this run.")
    ARCHIVE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_INDEX_PATH.write_text("\n".join(archive_lines) + "\n", encoding="utf-8")

    # Cleanup index retains previous runs and links this run.
    old_index = CLEANUP_INDEX_PATH.read_text(encoding="utf-8") if CLEANUP_INDEX_PATH.exists() else "# Cleanup History\n\n"
    link = f"- [{run_id}]({run_id}/REPORT.md) — current-state cleanup from `{base_sha}`\n"
    if link not in old_index:
        old_index += ("\n" if not old_index.endswith("\n") else "") + link
    CLEANUP_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLEANUP_INDEX_PATH.write_text(old_index, encoding="utf-8")

    # Recompute current tracked set after all generated files.
    run_dir_abs = root / run_dir
    run_dir_abs.mkdir(parents=True, exist_ok=True)

    write_json(run_dir_abs / "RELOCATION_MANIFEST.json", {
        "schema_version": "BV-RELOCATION-1",
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "run_id": run_id,
        "operations": operations,
        "placement_decisions": placement,
    })
    write_json(run_dir_abs / "PROTECTED_INVENTORY.json", {
        "schema_version": "BV-PROTECTED-1",
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "run_id": run_id,
        "records": protected_inventory,
    })

    # Bounded verification.
    checks: list[tuple[str, list[str]]] = [
        ("git-diff-check", ["git", "diff", "--check"]),
        ("json-registry", [sys.executable, "-c", "import json;json.load(open('bubbleverse_program_registry.json',encoding='utf-8'));print('PASS')"]),
        ("compile-cleanup-engine", [sys.executable, "-m", "py_compile", "tools/maintenance/bubbleverse_cleanup_current_v2.py"]),
    ]
    for cid, cmd in checks:
        cp = run(cmd, root, check=False)
        state = "PASS" if cp.returncode == 0 else "FAIL"
        validation.append(
            {
                "check_id": cid,
                "command": cmd,
                "status": state,
                "exit_code": cp.returncode,
                "stdout": cp.stdout[-4000:],
                "stderr": cp.stderr[-4000:],
            }
        )
        if cp.returncode:
            raise RuntimeError(f"Verification failed: {cid}\n{cp.stdout}\n{cp.stderr}")

    # Verify archived files no longer live in active workflow discovery and byte identities match.
    for op in operations:
        old = root / op["old_path"]
        new = root / op["new_path"]
        ok = (not old.exists()) and new.exists() and sha256_file(new) == op["source_sha256"]
        validation.append(
            {
                "check_id": f"archive-integrity-{op['operation_id']}",
                "status": "PASS" if ok else "FAIL",
                "old_path": op["old_path"],
                "new_path": op["new_path"],
            }
        )
        need(ok, f"Archive integrity failed for {op['old_path']}")

    write_json(run_dir_abs / "VALIDATION_RESULTS.json", {
        "schema_version": "BV-VALIDATION-1",
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "run_id": run_id,
        "checks": validation,
    })

    after = tracked_files(root)
    root_after = sorted(p for p in after if "/" not in p)
    diff_names = run(["git", "status", "--short"], root).stdout.splitlines()

    outcome = "CLEANUP_VERIFIED" if (all(x["status"] == "PASS" for x in validation) and deferred_count == 0) else "CLEANUP_PARTIALLY_VERIFIED"
    report = [
        f"# Bubbleverse Repository Cleanup — {run_id}",
        "",
        f"Outcome: **{outcome}**",
        "",
        f"Delivery state: **INSTALLATION_PACKAGE_READY / local workflow candidate**",
        "",
        f"- Repository: `{REPOSITORY}`",
        f"- BASE_SHA: `{base_sha}`",
        f"- Engine: `{ENGINE_VERSION}`",
        f"- Prompt contract: `{PROMPT_ID}` v{PROMPT_VERSION}",
        f"- Mode: `{mode}`",
        f"- Tracked files before: {len(before)}",
        f"- Root files before: {len(root_before)}",
        f"- Root files after: {len(root_after)}",
        f"- Archived payload moves: {len(operations)}",
        f"- Deferred retirement candidates: {deferred_count}",
        "",
        "## Safety boundary",
        "",
        "Only registry-backed retired program/workflow paths with explicit supersession evidence and no active/shared/incoming dependency blockers were archived.",
        "Journals, results, datasets, provenance records, preregisters, source locks and ambiguous historical files were not auto-moved.",
        "",
        "## Changed paths",
        "",
    ]
    report += [f"- `{x}`" for x in diff_names] or ["- None"]
    report += [
        "",
        "## Verification",
        "",
    ]
    report += [f"- {x['check_id']}: **{x['status']}**" for x in validation]
    report += [
        "",
        "## Next action",
        "",
        "Run the companion GitHub Actions workflow in `preview` first. If the artifact/report is satisfactory, run `apply` to publish a separate cleanup branch and open a pull request. The workflow never auto-merges.",
        "",
    ]
    (run_dir_abs / "REPORT.md").write_text("\n".join(report), encoding="utf-8")

    write_json(run_dir_abs / "RUN_MANIFEST.json", {
        "schema_version": "BV-RUN-1",
        "run_id": run_id,
        "prompt_id": PROMPT_ID,
        "prompt_version": PROMPT_VERSION,
        "engine_version": ENGINE_VERSION,
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "mode": mode,
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "target_q": "UNSET",
        "operations": len(operations),
        "deferred": deferred_count,
        "outcome": outcome,
        "delivery_state": "LOCAL_WORKFLOW_CANDIDATE",
    })

    # Delivery manifest includes final hashes of generated evidence files.
    payloads = []
    for rel in [
        "README.md",
        "START_CODES.md",
        "docs/REPOSITORY_STRUCTURE.md",
        "archive/programs/INDEX.md",
        "docs/maintenance/cleanup/INDEX.md",
        str(run_dir / "REPORT.md"),
        str(run_dir / "RELOCATION_MANIFEST.json"),
        str(run_dir / "PROTECTED_INVENTORY.json"),
        str(run_dir / "VALIDATION_RESULTS.json"),
        str(run_dir / "RUN_MANIFEST.json"),
    ]:
        p = root / rel
        if p.exists() and p.is_file():
            payloads.append({"path": rel, "sha256": sha256_file(p), "action": "ADD_OR_UPDATE"})
    if archived_by_record:
        payloads.append({"path": str(REGISTRY_PATH), "sha256": sha256_file(root / REGISTRY_PATH), "action": "UPDATE"})
    write_json(run_dir_abs / "DELIVERY_MANIFEST.json", {
        "schema_version": "BV-DELIVERY-1",
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "run_id": run_id,
        "payloads": payloads,
        "archive_operations": operations,
    })

    # Stage everything only after all gates pass.
    run(["git", "add", "-A"], root)
    run(["git", "diff", "--cached", "--check"], root)

    changed = run(["git", "diff", "--cached", "--quiet"], root, check=False).returncode == 1
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"run_id={run_id}\n")
            f.write(f"base_sha={base_sha}\n")
            f.write(f"report_path={run_dir}/REPORT.md\n")

    print(json.dumps({
        "outcome": outcome,
        "repository": REPOSITORY,
        "base_sha": base_sha,
        "run_id": run_id,
        "changed": changed,
        "archive_moves": len(operations),
        "deferred": deferred_count,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
