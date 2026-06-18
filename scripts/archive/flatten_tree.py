#!/usr/bin/env python3
"""
Flatten single-page leaf directories to remove one nav level.

A "leaf" directory contains only index.md and no sub-directories.
Converting dir/index.md → dir.md (sibling) keeps the URL identical
(MkDocs use_directory_urls: true maps both to /dir/).

When the file moves up one directory, relative links lose one ../ prefix:
  ../sibling/  →  sibling/
  ../../parent/  →  ../parent/

Run with --dry-run first to preview changes.
"""

import os, re, shutil, sys
from pathlib import Path

DOCS = Path("docs")
DRY = "--dry-run" in sys.argv
MIN_DEPTH = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--depth=")), "5"))

KEEP_AS_SECTION = {
    "architecture", "deploy", "operations", "troubleshooting",
    "security", "internals", "topics", "learning-path",
    "monitoring", "automation", "backup", "dr",
}

REL_LINK = re.compile(r'(\[.*?\]\()(\.\./|(?!http|#|/)[^)]+/)([^)]*\))')


def fix_relative_links(content: str) -> str:
    """Strip one ../ level from relative links (file moved up one dir)."""
    def _fix(m):
        prefix = m.group(2)  # the leading ../
        if prefix == "../":
            # remove one level — sibling becomes same-dir
            return m.group(1) + m.group(3)
        if prefix.startswith("../"):
            return m.group(1) + prefix[3:] + m.group(3)
        # link has no leading ../ — it was pointing into a sub-dir of old location
        # now needs ../ to reach the same place from parent
        return m.group(1) + "../" + prefix + m.group(3)
    return REL_LINK.sub(_fix, content)


moved = skipped = 0

candidates = []
for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted(d for d in dirs if not d.startswith("."))
    path = Path(root)
    if "index.md" not in files:
        continue
    has_children = any(
        (path / d / "index.md").exists()
        for d in os.listdir(root)
        if os.path.isdir(path / d)
    )
    if has_children:
        continue
    depth = len(path.relative_to(DOCS).parts)
    if depth < MIN_DEPTH:
        continue
    if path.name in KEEP_AS_SECTION:
        continue
    candidates.append(path)

print(f"Candidates: {len(candidates)}  (depth ≥ {MIN_DEPTH}, dry={DRY})")

for path in sorted(candidates):
    src = path / "index.md"
    dst = path.parent / f"{path.name}.md"
    if dst.exists():
        print(f"  SKIP (target exists): {dst.relative_to(DOCS)}")
        skipped += 1
        continue
    if not DRY:
        content = src.read_text(encoding="utf-8")
        fixed = fix_relative_links(content)
        dst.write_text(fixed, encoding="utf-8")
        os.remove(str(src))
        try:
            os.rmdir(str(path))
        except OSError:
            print(f"  WARN: dir not empty after move: {path.relative_to(DOCS)}")
    moved += 1

if DRY:
    print(f"\nWould move: {moved}   Skipped: {skipped}")
else:
    print(f"\nMoved: {moved}   Skipped: {skipped}")
