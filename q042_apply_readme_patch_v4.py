#!/usr/bin/env python3
"""Differential README synchronization for the canonical Bubbleverse launcher."""
from pathlib import Path

p=Path("README.md")
text=p.read_text(encoding="utf-8")
old="2. Select **000 🚀 BUBBLEVERSE START — SEGMENTED V5**"
new="2. Select **🚀 BUBBLEVERSE START**"

if old in text:
    text=text.replace(old,new,1)
elif new not in text:
    raise SystemExit("README_LAUNCHER_TEXT_GATE=FAIL")

anchor="The repository includes a central launcher for registered programs.\n"
extra="\nThe canonical launcher file is:\n\n```text\n.github/workflows/00-bubbleverse-start.yml\n```\n"
if ".github/workflows/00-bubbleverse-start.yml" not in text:
    if anchor not in text:
        raise SystemExit("README_CANONICAL_LAUNCHER_ANCHOR_GATE=FAIL")
    text=text.replace(anchor,anchor+extra,1)

p.write_text(text,encoding="utf-8")
print("README_GATE=PASS")
