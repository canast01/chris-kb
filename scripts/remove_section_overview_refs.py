#!/usr/bin/env python3
"""
remove_section_overview_refs.py — Remove img references to Section Overview
SVG files from all markdown pages.

Finds every SVG in docs/assets/ that contains "Section Overview", then
strips the referencing ![](...) or <img src="..."> lines from .md files.
Also removes the SVG files themselves.
"""

import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
ASSETS = DOCS / "assets"

IMG_MD   = re.compile(r"!\[[^\]]*\]\([^)]*\.svg\)")
IMG_HTML = re.compile(r'<img\s[^>]*src="[^"]*\.svg"[^>]*/?\s*>')


def bad_svg_names() -> set[str]:
    names = set()
    for svg in ASSETS.glob("*.svg"):
        try:
            if "Section Overview" in svg.read_text(encoding="utf-8", errors="ignore"):
                names.add(svg.name)
        except Exception:
            pass
    return names


def process_file(path: Path, bad: set[str]) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    new_lines = []
    removed = 0
    for line in lines:
        # Check if this line references any bad SVG
        matched = False
        for pat in (IMG_MD, IMG_HTML):
            m = pat.search(line)
            if m and any(b in m.group(0) for b in bad):
                matched = True
                break
        if matched:
            removed += 1
        else:
            new_lines.append(line)

    if removed:
        new_text = "".join(new_lines)
        new_text = re.sub(r"^\n+", "", new_text)       # strip leading blanks
        new_text = re.sub(r"\n{3,}", "\n\n", new_text)  # collapse internal blanks
        path.write_text(new_text, encoding="utf-8")
    return removed


def main():
    bad = bad_svg_names()
    print(f"Found {len(bad)} Section Overview SVG files")

    md_files_fixed = md_refs_removed = 0
    for md in sorted(DOCS.rglob("*.md")):
        count = process_file(md, bad)
        if count:
            md_files_fixed += 1
            md_refs_removed += count

    # Delete the SVG files
    for name in bad:
        (ASSETS / name).unlink(missing_ok=True)

    print(f"Removed {md_refs_removed} img references from {md_files_fixed} .md files")
    print(f"Deleted {len(bad)} Section Overview SVG asset files")


if __name__ == "__main__":
    main()
